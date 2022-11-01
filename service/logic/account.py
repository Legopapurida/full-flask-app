from typing import Dict
from service.data import layer_manager, mongo_user_layer
from service import Application as root
from service.core.loaders import UserModel
from odmantic import ObjectId
from flask import g

layer = layer_manager.layers[mongo_user_layer]


class AccountLogics:
    def add_new_user(self, data: Dict):
        current_user: UserModel = g.user
        user = layer.get_user_by_id(ObjectId(current_user.id))
        sub_user = layer.add_sub_user(user=user, sub_user_data=data)
        return sub_user.dict()

    def get_registered_users(self):
        current_user: UserModel = g.user
        user = layer.get_user_by_id(ObjectId(current_user.id))

        return user.dict()
