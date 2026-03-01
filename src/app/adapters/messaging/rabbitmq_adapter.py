from typing import Protocol

from src.app.domain.entities.event_message import EventMessage
from src.app.infra.messaging.rabbitmq_manager import (
    InfraEventMessage,
    RabbitMQPort,
)


class RabbitMQAdapterPort(Protocol):
    async def publish(self, event_message: EventMessage) -> None: ...
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...


class RabbitMQAdapter(RabbitMQAdapterPort):
    def __init__(self, rabbitmq_manager: RabbitMQPort):
        self.rabbitmq_manager = rabbitmq_manager

    async def connect(self):
        await self.rabbitmq_manager.connect()

    async def publish(self, event_message: EventMessage):
        infra_message = InfraEventMessage(
            event_name=event_message.event_name,
            data=event_message.data,
        )
        await self.rabbitmq_manager.publish(infra_message)

    async def disconnect(self) -> None:
        await self.rabbitmq_manager.disconnect()
