from typing import Protocol

from src.app.domain.entities.event_message import PublishEventMessageInput


class EventPublisherPort(Protocol):
    async def publish(
        self, publish_event_message_input: PublishEventMessageInput
    ) -> None: ...
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
