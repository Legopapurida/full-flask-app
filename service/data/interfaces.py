from __future__ import annotations
from abc import abstractmethod, ABC


class UserDataLayer(ABC):
    @abstractmethod
    def save(self, **kwargs):
        ...

    @abstractmethod
    def get_user_by_username(self, username: str):
        ...

    @abstractmethod
    def get_user_by_id(self, user_id: Any):
        ...
