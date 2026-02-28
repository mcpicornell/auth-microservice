from src.app.domain.entities.token import (
    CreateTokenInput,
    CreateTokenOutput,
    DecodedToken,
)
from src.app.domain.ports.token_provider_port import TokenProviderPort
from src.app.infra.auth.jwt_manager import JWTPort


class JWTAdapter(TokenProviderPort):
    def __init__(self, jwt_manager: JWTPort):
        self.jwt_manager = jwt_manager

    def create_access_token(self, input_data: CreateTokenInput) -> CreateTokenOutput:
        access_token = self.jwt_manager.create_access_token(
            input_data.user_id, input_data.email
        )

        return CreateTokenOutput(
            access_token=access_token,
            refresh_token="",
            expires_in=0,
            token_type="bearer",
        )

    def create_refresh_token(self, input_data: CreateTokenInput) -> CreateTokenOutput:
        refresh_token = self.jwt_manager.create_refresh_token(
            input_data.user_id, input_data.email
        )

        return CreateTokenOutput(
            access_token="",
            refresh_token=refresh_token,
            expires_in=0,
            token_type="bearer",
        )

    def decode_token(self, token: str) -> DecodedToken:
        return self.jwt_manager.decode_token(token)

    def verify_token(self, token: str) -> bool:
        return self.jwt_manager.verify_token(token)
