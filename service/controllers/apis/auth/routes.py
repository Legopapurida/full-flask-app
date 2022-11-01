from typing import Dict
from flask.views import MethodView
from flask_smorest import abort
from flask import session
from . import router
from . import income
from . import outcome
from service.logic.auth import AuthenticationLogics


@router.route("/register")
class Register(MethodView):
    @router.arguments(income.RegisterSchema)
    @router.response(201, outcome.RegisterSchema)
    def post(self, user_data: Dict):
        result = AuthenticationLogics().register_user(data=user_data)
        return result


@router.route("/login")
class Login(MethodView):
    @router.arguments(income.LoginSchema)
    @router.response(200)
    def post(self, user_data: Dict):
        result = AuthenticationLogics().login_user(data=user_data)
        if result:
            session["aid"] = result["aid"]
            return result
        abort(404)


@router.route("/logout")
class Logout(MethodView):
    @router.response(200)
    def get(self):
        session.clear()
        return "user logged out"
