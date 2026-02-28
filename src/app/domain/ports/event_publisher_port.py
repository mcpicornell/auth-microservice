from abc import ABC, abstractmethod

from src.app.domain.entities.event_message import EventMessage


class EventPublisherPort(ABC):
    @abstractmethod
    async def publish(self, event_message: EventMessage) -> None:
        pass

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass
