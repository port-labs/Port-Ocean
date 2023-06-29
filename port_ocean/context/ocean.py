from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING, Any

from fastapi import APIRouter
from werkzeug.local import LocalProxy, LocalStack

from port_ocean.clients.port.client import PortClient
from port_ocean.clients.port.types import UserAgentType
from port_ocean.config.integration import IntegrationConfiguration
from port_ocean.core.models import Entity
from port_ocean.core.types import (
    RESYNC_EVENT_LISTENER,
    START_EVENT_LISTENER,
    RawEntityDiff,
)
from port_ocean.errors import PortOceanContextNotFoundError

if TYPE_CHECKING:
    from port_ocean.core.integrations.base import BaseIntegration
    from port_ocean.port_ocean import Ocean


@dataclass
class PortOceanContext:
    app: "Ocean"

    @property
    def config(self) -> IntegrationConfiguration:
        return self.app.config

    @property
    def router(self) -> APIRouter:
        return self.app.integration_router

    @property
    def integration(self) -> "BaseIntegration":
        return self.app.integration

    @property
    def integration_config(self) -> dict[str, Any]:
        return self.app.config.integration.config

    @property
    def port_client(self) -> PortClient:
        return self.app.port_client

    def on_resync(
        self,
        kind: str | None = None,
    ) -> Callable[[RESYNC_EVENT_LISTENER], RESYNC_EVENT_LISTENER]:
        def wrapper(function: RESYNC_EVENT_LISTENER) -> RESYNC_EVENT_LISTENER:
            return self.integration.on_resync(function, kind)

        return wrapper

    def on_start(self) -> Callable[[START_EVENT_LISTENER], START_EVENT_LISTENER]:
        def wrapper(function: START_EVENT_LISTENER) -> START_EVENT_LISTENER:
            return self.integration.on_start(function)

        return wrapper

    async def update_raw_diff(
        self,
        kind: str,
        raw_diff: RawEntityDiff,
        user_agent_type: UserAgentType = UserAgentType.exporter,
    ) -> None:
        await self.integration.update_raw_diff(kind, raw_diff, user_agent_type)

    async def register_raw(
        self,
        kind: str,
        change: list[dict[str, Any]],
        user_agent_type: UserAgentType = UserAgentType.exporter,
    ) -> None:
        await self.integration.register_raw(kind, change, user_agent_type)

    async def unregister_raw(
        self,
        kind: str,
        change: list[dict[str, Any]],
        user_agent_type: UserAgentType = UserAgentType.exporter,
    ) -> None:
        await self.integration.unregister_raw(kind, change, user_agent_type)

    async def register(
        self,
        entities: list[Entity],
        user_agent_type: UserAgentType = UserAgentType.exporter,
    ) -> None:
        await self.integration.register(entities, user_agent_type)

    async def unregister(
        self,
        entities: list[Entity],
        user_agent_type: UserAgentType = UserAgentType.exporter,
    ) -> None:
        await self.integration.unregister(entities, user_agent_type)

    async def sync(
        self, entities: list[Entity], user_agent_type: UserAgentType
    ) -> None:
        await self.integration.sync(entities, user_agent_type)

    async def sync_all(self) -> None:
        await self.integration.sync_all(trigger_type="manual")


_port_ocean_context_stack: LocalStack[PortOceanContext] = LocalStack()


def initialize_port_ocean_context(ocean_app: "Ocean") -> None:
    """
    This Function initiates the PortOcean context and pushes it into the LocalStack().
    """
    _port_ocean_context_stack.push(PortOceanContext(app=ocean_app))


def _get_port_ocean_context() -> PortOceanContext:
    """
    Get the PortOcean context from the current thread.
    """
    port_ocean_context = _port_ocean_context_stack.top
    if port_ocean_context is not None:
        return port_ocean_context

    raise PortOceanContextNotFoundError(
        "You must first initialize PortOcean in order to use it"
    )


ocean: PortOceanContext = LocalProxy(lambda: _get_port_ocean_context())  # type: ignore
