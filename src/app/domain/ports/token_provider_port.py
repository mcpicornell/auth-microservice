from abc import ABC, abstractmethod

from src.app.domain.entities.token import (
    CreateTokenInput,
    CreateTokenOutput,
    DecodedToken,
)


class TokenProviderPort(ABC):
    @abstractmethod
    def create_access_token(self, input_data: CreateTokenInput) -> CreateTokenOutput:
        pass

    @abstractmethod
    def create_refresh_token(self, input_data: CreateTokenInput) -> CreateTokenOutput:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> DecodedToken:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> bool:
        pass
