from typing import List, Tuple, Any, Union

import yaml
from gitlab import Gitlab, GitlabList
from gitlab.base import RESTObject
from gitlab.v4.objects import Project
from loguru import logger

from gitlab_integration.core.entities import generate_entity_from_port_yaml
from gitlab_integration.core.utils import does_pattern_apply
from port_ocean.core.models import Entity


class GitlabService:
    def __init__(
        self,
        gitlab_client: Gitlab,
        app_host: str,
        group_mapping: List[str],
    ):
        self.gitlab_client = gitlab_client
        self.app_host = app_host
        self.group_mapping = group_mapping

    def _is_exists(self, group: RESTObject) -> bool:
        for hook in group.hooks.list(iterator=True):
            if hook.url == f"{self.app_host}/integration/hook/{group.get_id()}":
                return True
        return False

    def _create_group_webhook(self, group: RESTObject) -> None:
        group.hooks.create(
            {
                "url": f"{self.app_host}/integration/hook/{group.get_id()}",
                "push_events": True,
                "merge_requests_events": True,
            }
        )

    def get_root_groups(self) -> List[RESTObject]:
        groups = self.gitlab_client.groups.list(iterator=True)
        return [group for group in groups if group.parent_id is None]

    def create_webhooks(self) -> list[int | str]:
        root_partial_groups = self.get_root_groups()
        filtered_partial_groups = [
            group
            for group in root_partial_groups
            if any(
                does_pattern_apply(mapping.split("/")[0], group.attributes["full_path"])
                for mapping in self.group_mapping
            )
        ]

        webhook_ids = []
        for partial_group in filtered_partial_groups:
            group_id = partial_group.get_id()
            if group_id is None:
                logger.info(
                    f"Group {partial_group.attributes['full_path']} has no id. skipping..."
                )
            else:
                if self._is_exists(partial_group):
                    logger.info(
                        f"Webhook already exists for group {partial_group.get_id()}"
                    )
                else:
                    self._create_group_webhook(partial_group)
                webhook_ids.append(group_id)

        return webhook_ids

    def _filter_mappings(self, projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            project
            for project in projects
            if all(
                does_pattern_apply(mapping, project["path_with_namespace"])
                for mapping in self.group_mapping
            )
        ]

    def get_group_projects(self, group_id: int | None = None) -> list[dict[str, Any]]:
        if group_id is None:
            return [
                project
                for group in self.gitlab_client.groups.list()
                for project in self.gitlab_client.groups.get(group.id).attributes[
                    "projects"
                ]
            ]
        group = self.gitlab_client.groups.get(group_id)
        projects: list[dict[str, Any]] = group.attributes["projects"]
        return [
            *projects,
            *[
                project
                for sub_group in group.subgroups.list()
                for project in self.get_group_projects(sub_group.id)
            ],
        ]

    def get_project(self, project_id: int) -> Project | None:
        logger.info(f"fetching project {project_id}")
        project = self.gitlab_client.projects.get(project_id)
        if all(
            does_pattern_apply(mapping, project.path_with_namespace)
            for mapping in self.group_mapping
        ):
            return project
        return None

    def get_all_projects(self) -> list[dict[str, Any]]:
        logger.info("fetching all projects for the token")
        projects = self.get_group_projects()

        return self._filter_mappings(projects)

    def _get_changed_files_between_commits(
        self, project_id: int, head: str
    ) -> Union[GitlabList, list[dict[str, Any]]]:
        project = self.gitlab_client.projects.get(project_id)
        return project.commits.get(head).diff()

    def _get_file_paths(
        self, project: Project, path: str | List[str], commit_sha: str
    ) -> list[str]:
        if not isinstance(path, list):
            path = [path]
        files = project.repository_tree(ref=commit_sha, all=True)
        return [
            file["path"]
            for file in files
            if does_pattern_apply(path, file["path"] or "")
        ]

    def _get_entities_from_git(
        self, project: Project, file_name: str, sha: str, ref: str
    ) -> List[Entity]:
        try:
            file_content = project.files.get(file_path=file_name, ref=sha)
            entities = yaml.safe_load(file_content.decode())
            raw_entities = [
                Entity(**entity_data)
                for entity_data in (
                    entities if isinstance(entities, list) else [entities]
                )
            ]
            return [
                generate_entity_from_port_yaml(entity_data, project, ref)
                for entity_data in raw_entities
            ]
        except Exception:
            return []

    def _get_entities_by_commit(
        self, project: Project, spec: str | List["str"], commit: str, ref: str
    ) -> List[Entity]:
        spec_paths = self._get_file_paths(project, spec, commit)
        return [
            entity
            for path in spec_paths
            for entity in self._get_entities_from_git(project, path, commit, ref)
        ]

    def get_entities_diff(
        self,
        project: Project,
        spec_path: str | List[str],
        before: str,
        after: str,
        ref: str,
    ) -> Tuple[List[Entity], List[Entity]]:
        entities_before = self._get_entities_by_commit(project, spec_path, before, ref)
        entities_after = self._get_entities_by_commit(project, spec_path, after, ref)

        return entities_before, entities_after
