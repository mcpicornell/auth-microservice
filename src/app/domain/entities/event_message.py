from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class EventMessage:
    event_name: str
    data: Dict[str, Any]
