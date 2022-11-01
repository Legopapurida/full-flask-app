from abc import ABC, abstractmethod
from typing import Any, Dict
from .configs import JWTConfigs


class TokenInterface(ABC):
    def __init__(self, configs: Dict) -> None:
        """Oauth Token Bearer Decoder

        Args:
            configs (Dict): configs
        """
        self.config = self.configure(configs)

    @abstractmethod
    def configure(self, configs: Dict) -> Any:
        ...

    @abstractmethod
    def parse_token(self, token: str) -> str:
        ...

    @abstractmethod
    def get_data(self, token: str) -> Dict:
        ...

    @abstractmethod
    def __call__(self) -> Dict:
        ...
