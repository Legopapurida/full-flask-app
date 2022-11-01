from typing import Dict
from odmantic import SyncEngine
from pymongo import MongoClient
from .interfaces import ExtensionInterface


class MongoDB(ExtensionInterface):
    database: SyncEngine = None

    def __init__(self, configs: Dict) -> None:
        self.configs: Dict = configs

    def __connect(self):
        if not self.database:
            self.database = SyncEngine(
                MongoClient(self.configs["MONGO_DATABASE_URI"]),
                database=self.configs["MONGO_DATABASE_NAME"],
            )

    def install_extension(self):
        self.__connect()
