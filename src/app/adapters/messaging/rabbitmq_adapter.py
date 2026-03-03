from typing import Protocol

from src.app.domain.entities.event_message import PublishEventMessageInput
from src.app.infra.messaging.rabbitmq_manager import (
    RabbitMQPort,
)
from src.app.infra.messaging.rabbitmq_types import EventMessage, UserData


class RabbitMQAdapterPort(Protocol):
    async def publish(
        self, publish_event_message_input: PublishEventMessageInput
    ) -> None: ...
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...


class RabbitMQAdapter(RabbitMQAdapterPort):
    def __init__(self, rabbitmq_manager: RabbitMQPort):
        self.rabbitmq_manager = rabbitmq_manager

    async def connect(self):
        await self.rabbitmq_manager.connect()

    async def publish(self, publish_event_message_input: PublishEventMessageInput):
        infra_message = EventMessage(
            event_name=publish_event_message_input.event_name,
            data=UserData(**publish_event_message_input.data.__dict__),
        )

        await self.rabbitmq_manager.publish(infra_message)

    async def disconnect(self) -> None:
        await self.rabbitmq_manager.disconnect()
