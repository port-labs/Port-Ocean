from loguru import logger
from port_ocean.context.ocean import ocean
from client import ServicenowClient, ObjectKind
from port_ocean.core.ocean_types import ASYNC_GENERATOR_RESYNC_TYPE

def initialize_client() -> ServicenowClient:
    return ServicenowClient(
        ocean.integration_config["servicenow_instance"],
        ocean.integration_config["servicenow_username"],
        ocean.integration_config["servicenow_password"],
    )

@ocean.on_resync()
async def on_resources_resync(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    logger.info(f"Listing Servicenow resource: {kind}")
    servicenow_client = initialize_client()

    try: 
        async for records in servicenow_client.get_paginated_resource(resource_kind=ObjectKind(kind)):
            logger.info(f"Received {kind} batch with {len(records)} records")
            yield records
    except ValueError:
        logger.error(f"Invalid resource kind: {kind}")
        raise


@ocean.on_start()
async def on_start() -> None:
    print("Starting Servicenow integration")
    servicenow_client = initialize_client()
    await servicenow_client.sanity_check()
