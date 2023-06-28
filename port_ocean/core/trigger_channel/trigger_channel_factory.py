from typing import Callable, Dict, Any, Awaitable

from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.base import BaseWithContext
from port_ocean.core.trigger_channel.base import (
    BaseTriggerChannel,
    TriggerChannelEvents,
)
from port_ocean.core.trigger_channel.http import (
    HttpTriggerChannel,
)
from port_ocean.core.trigger_channel.settings import (
    HttpTriggerChannelSettings,
    KafkaTriggerChannelSettings,
)
from port_ocean.core.trigger_channel.kafka import (
    KafkaTriggerChannel,
)


class TriggerChannelFactory(BaseWithContext):
    def __init__(
        self,
        context: PortOceanContext,
        installation_id: str,
        events: TriggerChannelEvents,
    ):
        super().__init__(context)
        self.installation_id = installation_id
        self._trigger_channel: BaseTriggerChannel | None = None
        self.events = events

    def on_event(
        self, callback: Callable[[Dict[Any, Any]], Awaitable[None]]
    ) -> Callable[[Dict[Any, Any]], Awaitable[None]]:
        async def wrapper(event: Dict[Any, Any]) -> None:
            integration_identifier = (
                event.get("diff", {}).get("after", {}).get("identifier")
            )

            if integration_identifier == self.installation_id:
                await callback(event)

        return wrapper

    async def create_trigger_channel(self) -> None:
        wrapped_events: TriggerChannelEvents = {
            "on_resync": self.on_event(self.events["on_resync"]),
            "on_action": self.on_event(self.events["on_action"]),
        }
        config = self.context.config.trigger_channel
        _type = config.type.lower()
        assert_message = "Invalid trigger channel config, expected KafkaTriggerChannelSettings and got {0}"

        match _type:
            case "kafka":
                assert isinstance(
                    config, KafkaTriggerChannelSettings
                ), assert_message.format(type(config))
                org_id = await self.context.port_client.get_org_id()
                self._trigger_channel = KafkaTriggerChannel(
                    wrapped_events,
                    config,
                    org_id,
                )

            case "webhook":
                assert isinstance(
                    config, HttpTriggerChannelSettings
                ), assert_message.format(type(config))
                self._trigger_channel = HttpTriggerChannel(
                    wrapped_events,
                    config,
                    self.installation_id,
                )

            case _:
                raise Exception(f"Trigger channel {_type} not supported")

        await self._trigger_channel.start()
