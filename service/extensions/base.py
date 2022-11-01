from typing import List
from .interfaces import ExtensionInterface


class ExtensionInstaller:
    def __init__(self, *extensions: List[ExtensionInterface]) -> None:
        self.extensions: List[ExtensionInterface] = extensions

    def install_extensions(self):
        for extension in self.extensions:
            extension.install_extension()
