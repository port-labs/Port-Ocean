from loguru import logger
from port_ocean.context.ocean import ocean
from port_ocean.core.ocean_types import RAW_RESULT, ASYNC_GENERATOR_RESYNC_TYPE
from client import ArgocdClient, ObjectKind, ResourceKindsWithSpecialHandling
from fastapi import Request


def init_client() -> ArgocdClient:
    return ArgocdClient(
        ocean.integration_config["token"],
        ocean.integration_config["server_url"],
    )


@ocean.on_resync()
async def on_resources_resync(kind: str) -> RAW_RESULT:
    if kind in iter(ResourceKindsWithSpecialHandling):
        logger.info(f"Kind {kind} has a special handling. Skipping...")
        return []
    else:
        argocd_client = init_client()
        return await argocd_client.get_resources(resource_kind=ObjectKind(kind))


@ocean.on_resync(kind=ResourceKindsWithSpecialHandling.DEPLOYMENT_HISTORY)
async def on_history_resync(kind: str) -> RAW_RESULT:
    argocd_client = init_client()

    return await argocd_client.get_deployment_history()


@ocean.on_resync(kind=ResourceKindsWithSpecialHandling.KUBERNETES_RESOURCE)
async def on_managed_k8s_resources_resync(kind: str) -> RAW_RESULT:
    argocd_client = init_client()

    return await argocd_client.get_kubernetes_resource()

@ocean.on_resync(kind=ResourceKindsWithSpecialHandling.MANAGED_RESOURCE)
async def on_managed_resources_resync(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    argocd_client = init_client()

    applications = await argocd_client.get_resources(
        resource_kind=ObjectKind.APPLICATION
    )
    for application in applications:
        managed_resources = await argocd_client.get_managed_resources(
            application_name=application["metadata"]["name"]
        )
        application_resource = [
            {**managed_resource, "__applicationId": application["metadata"]["uid"]}
            for managed_resource in managed_resources
        ]
        yield application_resource


@ocean.router.post("/webhook")
async def on_application_event_webhook_handler(request: Request) -> None:
    data = await request.json()
    logger.debug(f"received webhook event data: {data}")
    argocd_client = init_client()

    if data["action"] == "upsert":
        application = await argocd_client.get_application_by_name(
            data["application_name"]
        )
        await ocean.register_raw(ObjectKind.APPLICATION, [application])
