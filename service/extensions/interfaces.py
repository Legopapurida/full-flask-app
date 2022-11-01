from abc import ABC
from abc import abstractmethod


class ExtensionInterface(ABC):
    @abstractmethod
    def install_extension(self) -> None:
        ...
