import asyncio
from typing import Type, Any

import httpx
from loguru import logger

from port_ocean.clients.port.client import PortClient
from port_ocean.clients.port.types import UserAgentType
from port_ocean.config.settings import IntegrationConfiguration
from port_ocean.context.ocean import ocean
from port_ocean.core.defaults.common import (
    Defaults,
    get_port_integration_defaults,
)
from port_ocean.core.handlers.port_app_config.models import PortAppConfig
from port_ocean.core.models import Blueprint
from port_ocean.core.utils.utils import gather_and_split_errors_from_results
from port_ocean.exceptions.port_defaults import (
    AbortDefaultCreationError,
)


def deconstruct_blueprints_to_creation_steps(
    raw_blueprints: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], ...]:
    """
    Deconstructing the blueprint into stages so the api wont fail to create a blueprint if there is a conflict
    example: Preventing the failure of creating a blueprint with a relation to another blueprint
    """
    (
        bare_blueprint,
        with_relations,
        full_blueprint,
    ) = ([], [], [])

    for blueprint in raw_blueprints.copy():
        full_blueprint.append(blueprint.copy())

        blueprint.pop("calculationProperties", {})
        blueprint.pop("mirrorProperties", {})
        blueprint.pop("aggregationProperties", {})
        with_relations.append(blueprint.copy())

        blueprint.pop("teamInheritance", {})
        blueprint.pop("relations", {})
        bare_blueprint.append(blueprint)

    return (
        bare_blueprint,
        with_relations,
        full_blueprint,
    )


async def _initialize_required_integration_settings(
    port_client: PortClient,
    default_mapping: PortAppConfig,
    integration_config: IntegrationConfiguration,
) -> None:
    try:
        logger.info("Initializing integration at port")
        integration = await port_client.get_current_integration(
            should_log=False, should_raise=False
        )
        if not integration:
            logger.info(
                "Integration does not exist, Creating new integration with default mapping"
            )
            integration = await port_client.create_integration(
                integration_config.integration.type,
                integration_config.event_listener.to_request(),
                port_app_config=default_mapping,
            )
        elif not integration.get("config"):
            logger.info(
                "Encountered that the integration's mapping is empty, Initializing to default mapping"
            )
            integration = await port_client.patch_integration(
                integration_config.integration.type,
                integration_config.event_listener.to_request(),
                port_app_config=default_mapping,
            )
    except httpx.HTTPStatusError as err:
        logger.error(f"Failed to apply default mapping: {err.response.text}.")
        raise err

    logger.info("Checking for diff in integration configuration")
    changelog_destination = integration_config.event_listener.to_request().get(
        "changelog_destination"
    )
    if (
        integration.get("changelogDestination") != changelog_destination
        or integration.get("installationAppType") != integration_config.integration.type
        or integration.get("version") != port_client.integration_version
    ):
        await port_client.patch_integration(
            integration_config.integration.type, changelog_destination
        )


async def _create_resources(
    port_client: PortClient,
    defaults: Defaults,
) -> None:
    creation_stage, *blueprint_patches = deconstruct_blueprints_to_creation_steps(
        defaults.blueprints
    )

    blueprints_results, _ = await gather_and_split_errors_from_results(
        [
            port_client.get_blueprint(blueprint["identifier"], should_log=False)
            for blueprint in creation_stage
        ],
        lambda item: isinstance(item, Blueprint),
    )

    if blueprints_results:
        logger.info(
            f"Blueprints already exist: {[result.identifier for result in blueprints_results]}. Skipping integration default creation..."
        )
        return

    created_blueprints, blueprint_errors = await gather_and_split_errors_from_results(
        (
            port_client.create_blueprint(
                blueprint, user_agent_type=UserAgentType.exporter
            )
            for blueprint in creation_stage
        )
    )

    created_blueprints_identifiers = [bp["identifier"] for bp in created_blueprints]

    if blueprint_errors:
        for error in blueprint_errors:
            if isinstance(error, httpx.HTTPStatusError):
                logger.warning(
                    f"Failed to create resources: {error.response.text}. Rolling back changes..."
                )

        raise AbortDefaultCreationError(
            created_blueprints_identifiers, blueprint_errors
        )

    try:
        for patch_stage in blueprint_patches:
            await asyncio.gather(
                *(
                    port_client.patch_blueprint(
                        blueprint["identifier"],
                        blueprint,
                        user_agent_type=UserAgentType.exporter,
                    )
                    for blueprint in patch_stage
                )
            )

    except httpx.HTTPStatusError as err:
        logger.error(f"Failed to create resources: {err.response.text}. continuing...")
        raise AbortDefaultCreationError(created_blueprints_identifiers, [err])
    try:
        created_actions, actions_errors = await gather_and_split_errors_from_results(
            (
                port_client.create_action(action, should_log=False)
                for action in defaults.actions
            )
        )

        created_scorecards, scorecards_errors = (
            await gather_and_split_errors_from_results(
                (
                    port_client.create_scorecard(
                        blueprint_scorecards["blueprint"], action, should_log=False
                    )
                    for blueprint_scorecards in defaults.scorecards
                    for action in blueprint_scorecards["data"]
                )
            )
        )

        created_pages, pages_errors = await gather_and_split_errors_from_results(
            (port_client.create_page(page, should_log=False) for page in defaults.pages)
        )

        errors = actions_errors + scorecards_errors + pages_errors
        if errors:
            for error in errors:
                if isinstance(error, httpx.HTTPStatusError):
                    logger.warning(
                        f"Failed to create resource: {error.response.text}. continuing..."
                    )

    except Exception as err:
        logger.error(f"Failed to create resources: {err}. continuing...")


async def _initialize_defaults(
    config_class: Type[PortAppConfig], integration_config: IntegrationConfiguration
) -> None:
    port_client = ocean.port_client
    defaults = get_port_integration_defaults(
        config_class, integration_config.resources_path
    )
    if not defaults:
        logger.warning("No defaults found. Skipping initialization...")
        return None

    if defaults.port_app_config:
        await _initialize_required_integration_settings(
            port_client, defaults.port_app_config, integration_config
        )

    if not integration_config.initialize_port_resources:
        return

    try:
        logger.info("Found default resources, starting creation process")
        await _create_resources(port_client, defaults)
    except AbortDefaultCreationError as e:
        logger.warning(
            f"Failed to create resources. Rolling back blueprints : {e.blueprints_to_rollback}"
        )
        await asyncio.gather(
            *(
                port_client.delete_blueprint(
                    identifier,
                    should_raise=False,
                    user_agent_type=UserAgentType.exporter,
                )
                for identifier in e.blueprints_to_rollback
            )
        )
        raise ExceptionGroup(str(e), e.errors)


def initialize_defaults(
    config_class: Type[PortAppConfig], integration_config: IntegrationConfiguration
) -> None:
    asyncio.new_event_loop().run_until_complete(
        _initialize_defaults(config_class, integration_config)
    )
