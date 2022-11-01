from typing import Optional
from sqlmodel import SQLModel
from sqlmodel import Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
