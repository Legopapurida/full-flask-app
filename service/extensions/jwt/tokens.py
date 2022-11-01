from typing import Dict
from jwt import DecodeError, ExpiredSignatureError, decode
from .exceptions import BearerInvalidTokenError
from .exceptions import InvalidTokenError
from .exceptions import ExpiredTokenError
from .configs import JWTConfigs
from .interfaces import TokenInterface
from .utils import decode64


class BearerToken(TokenInterface):
    def configure(self, configs: Dict) -> JWTConfigs:
        if (
            "SECRET_KEY" not in configs
            or "PUBLIC_KEY" not in configs
            or "PRIVATE_KEY" not in configs
        ):
            raise RuntimeError(f"{self.__class__.__name__} need secret key")
        return JWTConfigs(
            JWT_ALGORITHM=configs["JWT_ALGORITHM"],
            JWT_SECRET=configs.get("SECRET_KEY", None),
            JWT_PRIVATE_KEY=configs.get("PRIVATE_KEY", None),
            JWT_PUBLIC_KEY=configs.get("PUBLIC_KEY", None),
            JWT_OPTIONS=configs.get("JWT_OPTIONS", None),
            JWT_KWARGS=configs.get("JWT_KWARGS", {}),
        )

    def parse_token(self, token: str) -> str:
        _token: str = token.split(" ")
        bearer, token_value = _token
        if bearer.lower() != "bearer":
            raise BearerInvalidTokenError("Invalid Token")
        return token_value

    def get_data(self, token: str) -> Dict:
        try:
            configs: JWTConfigs = self.config
            key = (
                configs.JWT_SECRET
                if not configs.JWT_PUBLIC_KEY
                else configs.JWT_PUBLIC_KEY
            )
            claim: dict = decode(
                token,
                key=key,
                algorithms=[configs.JWT_ALGORITHM],
                options=configs.JWT_OPTIONS,
                audience=configs.JWT_KWARGS.get("JWT_AUDIENCE", None),
                issuer=configs.JWT_KWARGS.get("JWT_ISSUER", None),
            )
            return claim
        except DecodeError:
            raise InvalidTokenError
        except ExpiredSignatureError:
            raise ExpiredTokenError

    def __call__(self, token: str) -> Dict:
        token: str = self.parse_token(token)
        claim: dict = self.get_data(token=token)
        return claim


class BasicToken(TokenInterface):
    def configure(self, configs: Dict) -> None:
        pass

    def parse_token(self, token: bytes) -> str:
        message: str = decode64(token)
        _token: str = message.split(" ")
        bearer, token_value = _token
        if bearer.lower() != "basic":
            raise InvalidTokenError("Invalid Token")
        return token_value

    def get_token(self, token: str) -> Dict:
        username, password = token.split(":")
        return dict(username=username, password=password)

    def __call__(self, token: bytes) -> Dict:
        token: str = self.parse_token(token)
        claim: dict = self.get_data(token=token)
        return claim
