from src.app.domain.entities.event_message import EventMessage
from src.app.domain.ports.event_publisher_port import EventPublisherPort
from src.app.infra.messaging.rabbitmq_manager import RabbitMQPort


class RabbitMQAdapter(EventPublisherPort):
    def __init__(self, rabbitmq_manager: RabbitMQPort):
        self.rabbitmq_manager = rabbitmq_manager

    async def publish(self, event_message: EventMessage) -> None:
        await self.rabbitmq_manager.publish(event_message)

    async def connect(self) -> None:
        await self.rabbitmq_manager.connect()

    async def disconnect(self) -> None:
        await self.rabbitmq_manager.disconnect()
