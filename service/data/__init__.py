from typing import Generic, Tuple, TypeVar
from .mongo import MongoUserDataLayer
from .postgres import PostgresUserDataLayer

T = TypeVar("T")


class DataLayer(Generic[T]):
    def __init__(self, layers: T) -> None:
        self.layers: T = layers


mongo_user_layer = 0
postgres_user_layer = 1

layer_manager: DataLayer[
    Tuple[
        MongoUserDataLayer,
        PostgresUserDataLayer,
    ],
] = DataLayer(
    [
        MongoUserDataLayer(),
        PostgresUserDataLayer(),
    ]
)
