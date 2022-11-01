from copy import deepcopy
from datetime import datetime, timedelta, timezone
from json import JSONEncoder
from typing import Any, Dict, List, NewType
from typing import Type
from jwt import encode
from jwt import decode

Token = NewType("Token", str)
Payload = NewType("Payload", Dict[str, Any])
Headers = NewType("Headers", Dict[str, Any])
AccessToken = NewType("AccessToken", Token)
RefreshToken = NewType("RefreshToken", Token)


class JwtManager:
    def __init__(
        self,
        key: str,
        access_token_expire: timedelta,
        refresh_token_expire: timedelta,
        algorithm: str | None = "HS256",
    ) -> None:
        self.key: str = key
        self.algorithm: str | None = algorithm
        self.access_token_expire: timedelta = access_token_expire
        self.refresh_token_expire: timedelta = refresh_token_expire

    def encode(
        self,
        payload: Payload,
        key: str | None = None,
        algorithm: str | None = None,
        headers: Dict | None = None,
        json_encoder: Type[JSONEncoder] | None = None,
    ) -> Token:
        return encode(
            payload=payload,
            key=key or self.key,
            algorithm=algorithm or self.algorithm,
            headers=headers,
            json_encoder=json_encoder,
        )

    def decode(
        self,
        jwt: Token,
        key: str | None = None,
        algorithms: List[str] | None = None,
        options: Dict | None = None,
        **kwargs: Any
    ) -> Payload:
        return decode(
            jwt=jwt,
            key=key or self.key,
            algorithms=algorithms or [self.algorithm],
            options=options,
            **kwargs
        )

    def generate_access_token(
        self, payload: Payload, headers: Headers = None
    ) -> AccessToken:
        claim = deepcopy(payload)
        now = datetime.now(timezone.utc)
        exp = now + self.access_token_expire
        if now > exp:
            claim.update({"exp": self.access_token_expire})
        else:
            claim.update({"exp": exp})
        return self.encode(payload=claim, headers=headers)

    def generate_refresh_token(self, payload: Payload) -> RefreshToken:
        claim = deepcopy(payload)
        now = datetime.now(timezone.utc)
        exp = now + self.refresh_token_expire
        if now > exp:
            claim.update({"exp": self.refresh_token_expire})
        else:
            claim.update({"exp": exp})
        return self.encode(payload=claim)
