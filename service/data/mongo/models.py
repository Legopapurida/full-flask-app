from typing import List, Optional
from odmantic import Model
from odmantic import EmbeddedModel
from odmantic import Field


class SubUser(EmbeddedModel):
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(Model):
    username: str = Field(unique=True)
    password: str
    email: str = Field(unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    sub_users: Optional[List[SubUser]] = []
