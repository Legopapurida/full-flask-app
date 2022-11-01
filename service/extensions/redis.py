from typing import Dict
from .interfaces import ExtensionInterface
from redis import Redis, ConnectionPool


class RedisDB(ExtensionInterface):
    client: Redis = None

    def __init__(self, configs: Dict) -> None:
        self.configs: Dict = configs

    def __connect(self) -> None:
        if not self.client:
            self.client = Redis.from_url(self.configs["REDIS_DATABASE_URI"])

    def install_extension(self) -> None:
        self.__connect()
