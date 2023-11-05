from typing import Any
from loguru import logger
from port_ocean.core.ocean_types import ASYNC_GENERATOR_RESYNC_TYPE
from port_ocean.context.ocean import ocean
import asyncio
from client import FirehydrantClient
from utils import ObjectKind


## Helper function to initialize the Firehydrant client
def init_client() -> FirehydrantClient:
    return FirehydrantClient(
        ocean.integration_config["api_url"],
        ocean.integration_config["token"],
        ocean.integration_config.get("app_host", None),
    )


## Enriches the incident report data
async def enrich_retrospective_with_incident_data(
    http_client: FirehydrantClient, semaphore: asyncio.Semaphore, report: dict[str, Any]
) -> dict[str, Any]:
    async with semaphore:
        tasks = await http_client.get_tasks_by_incident(report["incident"]["id"])
        report["__incident"] = {"tasks": tasks}
        return report


@ocean.on_resync(ObjectKind.ENVIRONMENT)
async def on_environment_resync(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    firehydrant_client = init_client()

    async for environments in firehydrant_client.get_paginated_resource(
        resource_type=ObjectKind.ENVIRONMENT
    ):
        logger.debug(f"Received batch with {len(environments)} environments")
        yield environments


@ocean.on_resync(ObjectKind.SERVICE)
async def on_service_resync(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    firehydrant_client = init_client()

    async for services in firehydrant_client.get_paginated_resource(
        resource_type=ObjectKind.SERVICE
    ):
        logger.debug(f"Received batch with {len(services)} services")
        enriched_services = await firehydrant_client.get_incident_milestones(
            services=services
        )
        yield enriched_services


@ocean.on_resync(ObjectKind.INCIDENT)
async def on_incident_resync(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    firehydrant_client = init_client()

    async for incidents in firehydrant_client.get_paginated_resource(
        resource_type=ObjectKind.INCIDENT
    ):
        logger.debug(f"Received batch with {len(incidents)} incidents")
        yield incidents


@ocean.on_resync(ObjectKind.RETROSPECTIVE)
async def on_retrospective_resync(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    firehydrant_client = init_client()

    async for reports in firehydrant_client.get_paginated_resource(
        ObjectKind.RETROSPECTIVE
    ):
        logger.debug(
            f"Received batch with {len(reports)} reports, getting their tasks completion status"
        )
        semaphore = asyncio.Semaphore(5)
        tasks = [
            enrich_retrospective_with_incident_data(
                firehydrant_client, semaphore, report
            )
            for report in reports
        ]
        enriched_reports = await asyncio.gather(*tasks)
        yield enriched_reports


@ocean.router.post("/webhook")
async def handle_firehydrant_webhook(webhook_data: dict[str, Any]) -> None:
    firehydrant_client = init_client()
    ## check for incident in the webhook data. Have a look at the sample webhook event payload https://firehydrant.com/docs/integration-guides/creating-webhooks/
    data = webhook_data["data"]
    if "incident" in data:
        incident_id = data["incident"]["id"]
        incident_data = await firehydrant_client.get_single_incident(
            incident_id=incident_id
        )
        await ocean.register_raw(ObjectKind.INCIDENT, [incident_data])

        ## attempt to register retrospective data only if the incident is in postmoterm_completed status
        if incident_data["current_milestone"] == "postmortem_completed":
            retrospective_data = await firehydrant_client.get_single_retrospective(
                report_id=incident_data["report_id"]
            )
            await ocean.register_raw(ObjectKind.RETROSPECTIVE, [retrospective_data])

    if "environments" in data:
        for environment in data["environments"]:
            environment_id = environment["id"]
            environment_data = await firehydrant_client.get_single_environment(
                environment_id=environment_id
            )
            await ocean.register_raw(ObjectKind.ENVIRONMENT, [environment_data])

    if "services" in data:
        for service in data["services"]:
            service_id = service["id"]
            service_data = await firehydrant_client.get_single_service(
                service_id=service_id
            )
            await ocean.register_raw(ObjectKind.SERVICE, service_data)

    logger.info("Webhook event processed")


@ocean.on_start()
async def on_start() -> None:
    if ocean.event_listener_type == "ONCE":
        logger.info("Skipping webhook subscription because the event listener is ONCE")
        return

    ## We are making the subscription of webhook optional. It will be triggered only when the user specifies the app_host variable
    if ocean.integration_config.get("app_host"):
        logger.info("Subscribing to Firehydrant webhooks")

        firehydrant_client = init_client()
        await firehydrant_client.create_webhooks_if_not_exists()

        logger.info("Subscribed to webhook incident events")
