from service.logic.account import AccountLogics
from . import router
from flask import render_template
from flask import g
from service.core.permissions import IsAuthenticated
from service.core.loaders import UserLoader
from service import Application as root
from service.data import layer_manager

layer = layer_manager.layers[0]


@router.get("/register")
def register():
    return render_template("register.html")


@router.get("/login")
def login():
    return render_template("login.html")


@router.get("/account")
@IsAuthenticated()
def account():
    user = AccountLogics().get_registered_users()
    user["id"] = str(user["id"])
    return render_template("account.html", user=user)


@router.get("/add-user")
@IsAuthenticated()
def add_user():
    return render_template("add_user.html", user=g.user)
