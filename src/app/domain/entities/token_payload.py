from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenPayload:
    sub: str
    email: str
    exp: datetime
    iat: datetime
    type: str
