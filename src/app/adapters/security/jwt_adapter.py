from typing import Protocol

from src.app.domain.entities.token import (
    CreateTokenInput,
    CreateTokenOutput,
    DecodedToken,
)
from src.app.infra.auth.jwt_manager import (
    JWTPort,
)


class JWTAdapterPort(Protocol):
    def create_access_token(
        self, input_data: CreateTokenInput
    ) -> CreateTokenOutput: ...
    def create_refresh_token(
        self, input_data: CreateTokenInput
    ) -> CreateTokenOutput: ...
    def decode_token(self, token: str) -> DecodedToken: ...
    def verify_token(self, token: str) -> bool: ...


class JWTAdapter(JWTAdapterPort):
    def __init__(self, jwt_manager: JWTPort):
        self.jwt_manager = jwt_manager

    def create_access_token(self, input_data: CreateTokenInput) -> CreateTokenOutput:
        token = self.jwt_manager.create_access_token(
            user_id=input_data.user_id, email=input_data.email
        )
        return CreateTokenOutput(
            access_token=token,
            refresh_token="",  # No refresh token in access token creation
            expires_in=1800,  # 30 minutes default
            token_type="bearer",
        )

    def create_refresh_token(self, input_data: CreateTokenInput) -> CreateTokenOutput:
        token = self.jwt_manager.create_refresh_token(
            user_id=input_data.user_id, email=input_data.email
        )
        return CreateTokenOutput(
            access_token="",
            refresh_token=token,
            expires_in=604800,  # 7 days default
            token_type="bearer",
        )

    def decode_token(self, token: str) -> DecodedToken:
        infra_token = self.jwt_manager.decode_token(token)
        return DecodedToken(
            sub=str(infra_token.user_id),
            email=infra_token.email,
            exp=int(infra_token.exp.timestamp()),
            iat=int(infra_token.iat.timestamp()),
            type=infra_token.type,
        )

    def verify_token(self, token: str) -> bool:
        return self.jwt_manager.verify_token(token)
