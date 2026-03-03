from dataclasses import dataclass
from typing import Union


@dataclass
class UserData:
    user_id: str
    email: str
    username: str


type EventData = Union[UserData]


@dataclass
class EventMessage:
    event_name: str
    data: EventData
