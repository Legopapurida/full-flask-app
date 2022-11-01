from ..interfaces import UserDataLayer
from .models import User
from service import Application as root
from sqlmodel import Session
from sqlmodel import select


class PostgresUserDataLayer(UserDataLayer):
    def save(self, **kwargs) -> User:
        user = User(**kwargs)
        with Session(root.postgres.database) as session:
            session.add(user)
            session.commit()
        return user

    def get_user_by_username(self, username: str) -> User:
        with Session(root.postgres.database) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).one_or_none()
        return user

    def get_user_by_id(self, user_id: int) -> User:
        with Session(root.postgres.database) as session:
            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).one_or_none()
        return user
