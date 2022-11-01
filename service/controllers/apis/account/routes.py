from typing import Dict
from flask.views import MethodView
from flask import g
from . import router
from . import income
from . import outcome
from service import Application as root
from service.logic.account import AccountLogics
from service.core.permissions import IsAuthenticated


@router.route("/register")
class Register(MethodView):
    decorators = [IsAuthenticated()]

    @router.arguments(income.AddUserSchema)
    @router.response(201, outcome.AddUserSchema)
    @root.limiter.limit("1/minute")
    def post(self, user_data: Dict):
        user = AccountLogics().add_new_user(data=user_data)
        return user


@router.route("/get-user")
class GetUser(MethodView):
    decorators = [IsAuthenticated()]

    def get(self):
        user = AccountLogics().get_registered_users()
        user["id"] = str(user["id"])
        return user
