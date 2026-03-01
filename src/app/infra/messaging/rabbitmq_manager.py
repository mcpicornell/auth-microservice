from dataclasses import dataclass
from typing import Any, Dict, Protocol

from aio_pika import Message, connect_robust


@dataclass
class InfraEventMessage:
    event_name: str
    data: Dict[str, Any]


class RabbitMQPort(Protocol):
    async def publish(self, event_message: InfraEventMessage) -> None: ...
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...


class RabbitMQManager:
    def __init__(self, host: str, port: int, user: str, password: str, vhost: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.vhost = vhost
        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        self.connection = await connect_robust(
            host=self.host,
            port=self.port,
            login=self.user,
            password=self.password,
            virtualhost=self.vhost,
        )

        self.channel = await self.connection.channel()

        # Declare exchange using the correct aio_pika API
        await self.channel.declare_exchange(
            name="auth_events", type="topic", durable=True
        )

    async def disconnect(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def publish(self, event_message: InfraEventMessage) -> None:
        if not self.connection:
            await self.connect()

        channel = await self.connection.channel()

        message_body = str(event_message.data).encode("utf-8")
        message = Message(message_body)

        await channel.default_exchange.publish(
            message, routing_key=event_message.event_name
        )
