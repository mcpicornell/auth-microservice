from typing import Protocol

from src.app.domain.entities.token import (
    CreateTokenInput,
    CreateTokenOutput,
    DecodedToken,
)


class TokenProviderPort(Protocol):
    def create_access_token(
        self, input_data: CreateTokenInput
    ) -> CreateTokenOutput: ...
    def create_refresh_token(
        self, input_data: CreateTokenInput
    ) -> CreateTokenOutput: ...
    def decode_token(self, token: str) -> DecodedToken: ...
    def verify_token(self, token: str) -> bool: ...
