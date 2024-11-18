from typing import Any
from loguru import logger
from fastapi import Request
from port_ocean.context.ocean import ocean
from port_ocean.core.ocean_types import ASYNC_GENERATOR_RESYNC_TYPE
from gitlab.client import GitLabClient
from gitlab.webhook_handler import WebhookHandler
from gitlab.helpers.utils import ObjectKind, ResourceKindsHandledViaWebhooks

@ocean.on_resync()
async def on_resources_resync(kind: str) -> None:
    logger.info(f"Received re-sync for kind {kind}")

    if kind == ObjectKind.PROJECT:
        return

    gitlab_client = GitLabClient.create_from_ocean_config()

    async for resources in gitlab_client.get_resources(kind):
        logger.info(f"Re-syncing {len(resources)} {kind}")
        yield resources

@ocean.on_resync(ObjectKind.PROJECT)
async def on_project_resync(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    logger.info("Project Re-sync req received")
    gitlab_client = GitLabClient.create_from_ocean_config()

    async for projects in gitlab_client.get_resources(ObjectKind.PROJECT, {"owned": "yes"}):
        logger.info(f"Re-syncing {len(projects)} projects")
        yield projects

@ocean.router.post("/webhook")
async def on_webhook_alert(request: Request) -> dict[str, Any]:
    token = request.headers.get("X-Gitlab-Token")
    if not token:
        return {"status": "error"}

    webhook_handler = WebhookHandler.create_from_ocean_config()

    if webhook_handler.verify_token(token) is not True:
        return {"status": "error"}

    payload = await request.json()

    event = request.headers.get("X-Gitlab-Event")
    if event == "System Hook":
        await webhook_handler.handle_event(payload, True)
    else:
        await webhook_handler.handle_event(payload)

    return {"status": "success"}

@ocean.on_start()
async def on_start() -> None:
    logger.info("Starting async-gitlab integration...")

    logger.info("Initializing webhook setup...")
    webhook_handler = WebhookHandler.create_from_ocean_config()
    await webhook_handler.setup()
