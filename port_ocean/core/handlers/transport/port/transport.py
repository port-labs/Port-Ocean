import asyncio
from itertools import chain

from loguru import logger

from port_ocean.clients.port.types import UserAgentType
from port_ocean.context.event import event
from port_ocean.core.handlers.manipulation.base import (
    EntityPortDiff,
)
from port_ocean.core.handlers.transport.base import BaseTransport
from port_ocean.core.handlers.transport.port.order_by_entities_dependencies import (
    order_by_entities_dependencies,
)
from port_ocean.core.handlers.transport.port.validate_entity_relations import (
    validate_entity_relations,
)
from port_ocean.core.utils import (
    is_same_entity,
    get_unique,
    get_port_diff,
)
from port_ocean.types import EntityDiff


class HttpPortTransport(BaseTransport):
    async def _update_entity_diff(
        self, diff: EntityPortDiff, user_agent_type: UserAgentType
    ) -> None:
        ordered_deleted_entities = order_by_entities_dependencies(diff.deleted)
        for entity in ordered_deleted_entities:
            await self.context.port_client.delete_entity(entity, user_agent_type)

        ordered_created_entities = reversed(
            order_by_entities_dependencies(diff.created)
        )
        for entity in ordered_created_entities:
            await self.context.port_client.upsert_entity(
                entity,
                event.port_app_config.get_port_request_options(),
                user_agent_type,
            )

        ordered_modified_entities = reversed(
            order_by_entities_dependencies(diff.modified)
        )
        for entity in ordered_modified_entities:
            await self.context.port_client.upsert_entity(
                entity,
                event.port_app_config.get_port_request_options(),
                user_agent_type,
            )

    async def _validate_delete_dependent_entities(self, diff: EntityPortDiff) -> None:
        logger.info("Validated deleted entities")
        if not event.port_app_config.delete_dependent_entities:
            deps = await asyncio.gather(
                *[
                    self.context.port_client.search_dependent_entities(entity)
                    for entity in diff.deleted
                ]
            )
            new_dependent = get_unique(
                [
                    entity
                    for entity in chain.from_iterable(deps)
                    if not any([is_same_entity(item, entity) for item in diff.deleted])
                ]
            )

            if new_dependent:
                raise Exception(
                    f"Must enable delete_dependent_entities flag or delete also dependent entities:"
                    f" {[(dep.blueprint, dep.identifier) for dep in new_dependent]}"
                )

    async def _validate_entity_diff(self, diff: EntityPortDiff) -> None:
        config = event.port_app_config
        await self._validate_delete_dependent_entities(diff)
        modified_or_created_entities = diff.modified + diff.created
        logger.info("Validating modified or created entities")

        await asyncio.gather(
            *[
                self.context.port_client.validate_entity_payload(
                    entity,
                    {
                        "merge": config.enable_merge_entity,
                        "create_missing_related_entities": config.create_missing_related_entities,
                    },
                )
                for entity in modified_or_created_entities
            ]
        )
        await validate_entity_relations(diff, self.context.port_client)

    async def update_diff(
        self,
        entities: EntityDiff,
        user_agent_type: UserAgentType | None = None,
    ) -> None:
        entities_diff = get_port_diff(entities["before"], entities["after"])

        logger.info(
            f"Registering entity diff (created: {len(entities_diff.created)}, deleted: {len(entities_diff.deleted)}, modified: {len(entities_diff.modified)})"
        )
        await self._validate_entity_diff(entities_diff)
        await self._update_entity_diff(
            entities_diff, user_agent_type or self.DEFAULT_USER_AGENT_TYPE
        )
