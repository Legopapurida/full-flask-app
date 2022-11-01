from dataclasses import dataclass
from typing import Dict


@dataclass
class JWTConfigs:
    JWT_ALGORITHM: str
    JWT_SECRET: str = None
    JWT_PUBLIC_KEY: str = None
    JWT_PRIVATE_KEY: str = None
    JWT_OPTIONS: Dict = None
    JWT_HEADERS: Dict = None
    JWT_KWARGS: Dict = None
