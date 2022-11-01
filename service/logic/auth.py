from typing import Dict, NewType, Union
from service.data import layer_manager, mongo_user_layer
from service import Application as root
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from uuid import uuid4

layer = layer_manager.layers[mongo_user_layer]
AID = NewType("AID", str)


class AuthenticationLogics:

    # Internal Logics
    def create_tokens(self, user: Dict) -> Dict:
        return dict(
            access_token=root.jwt.generate_access_token(user),
            refresh_token=root.jwt.generate_refresh_token(user),
        )

    # API Logics
    def register_user(self, data: Dict) -> Dict:
        data["password"] = generate_password_hash(data["password"])
        result = layer.save(**data)
        return result.dict()

    def login_user(self, data: Dict) -> Union[AID, None]:
        user = layer.get_user_by_username(username=data["username"])
        if user:
            if check_password_hash(user.password, data["password"]):
                aid = str(uuid4())
                user_data = user.dict()
                user_data["id"] = str(user_data["id"])
                root.redis.client.hsetnx(
                    "users", aid, str(self.create_tokens(user=user_data))
                )
                return dict(aid=aid, username=user.username)
        return None
