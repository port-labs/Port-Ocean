import typing
from typing import Any
from enum import StrEnum

from loguru import logger
from gitlab.v4.objects import Project

from gitlab_integration.core.utils import generate_ref, does_pattern_apply
from gitlab_integration.events.hooks.base import ProjectHandler
from gitlab_integration.git_integration import GitlabPortAppConfig
from gitlab_integration.utils import ObjectKind

from port_ocean.clients.port.types import UserAgentType
from port_ocean.context.event import event
from port_ocean.context.ocean import ocean


class FileAction(StrEnum):
    DELETED = "deleted"
    ADDED = "added"
    MODIFIED = "modified"


class PushHook(ProjectHandler):
    events = ["Push Hook"]
    system_events = ["push"]

    async def _on_hook(self, body: dict[str, Any], gitlab_project: Project) -> None:
        commit_before, commit_after, ref = (
            body.get("before"),
            body.get("after"),
            body.get("ref"),
        )

        if commit_before is None or commit_after is None or ref is None:
            raise ValueError(
                "Invalid push hook. Missing one or more of the required fields (before, after, ref)"
            )

        added_files = [
            added_file
            for commit in body.get("commits", [])
            for added_file in commit.get("added", [])
        ]
        modified_files = [
            modified_file
            for commit in body.get("commits", [])
            for modified_file in commit.get("modified", [])
        ]

        removed_files = [
            removed_file
            for commit in body.get("commits", [])
            for removed_file in commit.get("removed", [])
        ]

        config: GitlabPortAppConfig = typing.cast(
            GitlabPortAppConfig, event.port_app_config
        )

        branch = config.branch or gitlab_project.default_branch

        if generate_ref(branch) == ref:
            spec_path = config.spec_path
            if not isinstance(spec_path, list):
                spec_path = [spec_path]

            await self._process_files(
                gitlab_project,
                removed_files,
                spec_path,
                commit_before,
                "",
                branch,
                FileAction.DELETED,
            )
            await self._process_files(
                gitlab_project,
                added_files,
                spec_path,
                "",
                commit_after,
                branch,
                FileAction.ADDED,
            )
            await self._process_files(
                gitlab_project,
                modified_files,
                spec_path,
                commit_before,
                commit_after,
                branch,
                FileAction.MODIFIED,
            )

            # update information regarding the project as well
            logger.info(
                f"Updating project information after push hook for project {gitlab_project.path_with_namespace}"
            )
            enriched_project = await self.gitlab_service.enrich_project_with_extras(
                gitlab_project
            )
            await ocean.register_raw(ObjectKind.PROJECT, [enriched_project])

        else:
            logger.debug(
                f"Skipping push hook for project {gitlab_project.path_with_namespace} because the ref {ref} "
                f"does not match the branch {branch}"
            )

    async def _process_files(
        self,
        gitlab_project: Project,
        files: list[str],
        spec_path: list[str],
        commit_before: str,
        commit_after: str,
        branch: str,
        file_action: FileAction,
    ) -> None:
        if not files:
            return
        logger.info(
            f"Processing {file_action} files {files} for project {gitlab_project.path_with_namespace}"
        )

        for file in files:
            try:
                if does_pattern_apply(spec_path, file):
                    logger.info(
                        f"Found file {file} in spec_path {spec_path} pattern, processing its entity diff"
                    )

                    if file_action == FileAction.DELETED:
                        entities_before = (
                            await self.gitlab_service._get_entities_by_commit(
                                gitlab_project, file, commit_before, branch
                            )
                        )
                        await ocean.update_diff(
                            {"before": entities_before, "after": []},
                            UserAgentType.gitops,
                        )

                    elif file_action == FileAction.ADDED:
                        entities_after = (
                            await self.gitlab_service._get_entities_by_commit(
                                gitlab_project, file, commit_after, branch
                            )
                        )
                        await ocean.update_diff(
                            {"before": [], "after": entities_after},
                            UserAgentType.gitops,
                        )

                    elif file_action == FileAction.MODIFIED:
                        entities_before = (
                            await self.gitlab_service._get_entities_by_commit(
                                gitlab_project, file, commit_before, branch
                            )
                        )
                        entities_after = (
                            await self.gitlab_service._get_entities_by_commit(
                                gitlab_project, file, commit_after, branch
                            )
                        )
                        await ocean.update_diff(
                            {"before": entities_before, "after": entities_after},
                            UserAgentType.gitops,
                        )
                else:
                    logger.info(
                        f"Skipping file {file} as it does not match the spec_path pattern {spec_path}"
                    )
            except Exception as e:
                logger.error(
                    f"Error processing file {file} in action {file_action}: {str(e)}"
                )
