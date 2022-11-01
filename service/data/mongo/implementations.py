from typing import Dict, List
from ..interfaces import UserDataLayer
from .models import User, SubUser
from service import Application as root
from odmantic import ObjectId


class MongoUserDataLayer(UserDataLayer):
    def save(self, **kwargs) -> User:
        return root.mongo.database.save(User(**kwargs))

    def get_user_by_username(self, username: str) -> User:
        user = root.mongo.database.find_one(User, User.username == username)
        return user

    def add_sub_user(self, user: User, sub_user_data: Dict) -> SubUser:
        sub_user = SubUser(**sub_user_data)
        user.sub_users.append(sub_user)
        root.mongo.database.save(user)
        return sub_user

    def get_user_by_id(self, user_id: ObjectId) -> User:
        return root.mongo.database.find_one(User, User.id == user_id)
