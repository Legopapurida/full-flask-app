from typing import Dict
from sqlmodel import create_engine, SQLModel
from sqlalchemy.future import Engine
from .interfaces import ExtensionInterface


def get_engine(self) -> Engine:
    return self


class PostgresDB(ExtensionInterface):
    database: Engine = None

    def __init__(self, configs: Dict) -> None:
        self.configs: Dict = configs

    def __connect(self):
        if not self.database:
            self.database = create_engine(self.configs["SQL_DATABASE_URI"], echo=False)

    def create_all(self):
        SQLModel.metadata.create_all(self.database)

    def drop_all(self):
        SQLModel.metadata.drop_all(self.database)

    def install_extension(self) -> None:
        self.__connect()
