from typing import Any
from loguru import logger

from gitlab.v4.objects import Project

from gitlab_integration.core.async_fetcher import AsyncFetcher
from gitlab_integration.events.hooks.base import ProjectHandler
from gitlab_integration.utils import ObjectKind
from port_ocean.context.ocean import ocean
import asyncio


class MergeRequest(ProjectHandler):
    events = ["Merge Request Hook"]
    system_events = ["merge_request"]

    async def _on_hook(self, body: dict[str, Any], gitlab_project: Project) -> None:
        logger.debug(
            f"Handling merge request hook for project {gitlab_project.path_with_namespace}, merge_request_id: {body.get('object_attributes', {}).get('iid')},"
            f" merge_request_title: {body.get('object_attributes', {}).get('title')}, status: {body.get('object_attributes', {}).get('state')}"
        )

        try:
            merge_requests = await asyncio.wait_for(
                AsyncFetcher.fetch_single(
                    gitlab_project.mergerequests.get,
                    body["object_attributes"]["iid"],
                ),
                timeout=10,
            )
            await ocean.register_raw(
                ObjectKind.MERGE_REQUEST, [merge_requests.asdict()]
            )
        except asyncio.TimeoutError:
            logger.error(
                f"Timeout while fetching merge request {body['object_attributes']['iid']} for project {gitlab_project.path_with_namespace}"
            )
