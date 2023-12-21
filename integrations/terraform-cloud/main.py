from enum import StrEnum
from typing import Any
from client import TerraformClient
from port_ocean.context.ocean import ocean
from loguru import logger
from asyncio import gather
from port_ocean.core.ocean_types import ASYNC_GENERATOR_RESYNC_TYPE


class ObjectKind(StrEnum):
    WORKSPACE = "workspace"
    RUN = "run"
    STATE_VERSION = "state-version"


def init_terraform_client() -> TerraformClient:
    """
    Intialize Terraform Client
    """
    config = ocean.integration_config
    
    terraform_client = TerraformClient(
                    config["terraform_host"],
                    config["terraform_token"],
                    )

    return terraform_client



@ocean.router.post("/webhook")
async def handle_webhook_request(data: dict[str, Any]) -> dict[str, Any]:
    terraform_client = init_terraform_client()

    run_id = data["run_id"]
    logger.info(f"Processing Terraform run event for run: {run_id}")

    workspace_id = data['workspace_id']
    logger.info(f"Processing Terraform run event for workspace: {workspace_id}")

    run, workspace = await gather(
        terraform_client.get_single_run(run_id),
        terraform_client.get_single_workspace(workspace_id)
    )

    await gather(
        ocean.register_raw(ObjectKind.RUN, [run]),
        ocean.register_raw(ObjectKind.WORKSPACE, [workspace])
    )

    logger.info("Terraform webhook event processed")
    return {"ok": True}


@ocean.on_resync(ObjectKind.WORKSPACE)
async def resync_workspaces(kind: str) -> list[dict[Any, Any]]:
    terraform_client = init_terraform_client()

    async for workspace in terraform_client.get_paginated_workspaces():
        logger.info(f"Received {len(workspace)} batch workspaces")
        yield workspace


@ocean.on_resync(ObjectKind.RUN)
async def resync_runs(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    terraform_client = init_terraform_client()

    async for workspaces in terraform_client.get_paginated_workspaces():
        logger.info(f"Received {len(workspaces)} batch runs")
        for workspace in workspaces:
            async for runs in terraform_client.get_paginated_runs_for_workspace(workspace['id']):
                yield runs


@ocean.on_resync(ObjectKind.STATE_VERSION)
async def resync_runs(kind:str)->ASYNC_GENERATOR_RESYNC_TYPE:
    terraform_client = init_terraform_client()

    async for state_versions in terraform_client.get_state_version_for_workspace():
            yield state_versions


@ocean.on_start()
async def on_start()-> None:
    logger.info("Starting Port Ocean Terraform integration")

    if ocean.event_listener_type == "ONCE":
        logger.info("Skipping webhook creation because the event listener is ONCE")
        return

    if not ocean.integration_config.get("app_host"):
        logger.warning(
            "No app host provided, skipping webhook creation. "
            "Without setting up the webhook, the integration will not export live changes from Terraform"
        )
        return

    terraform_client = init_terraform_client()
    await terraform_client.create_workspace_webhook(app_host=app_host)