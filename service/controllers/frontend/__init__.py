from flask import Blueprint


router = Blueprint("site", __name__, url_prefix="/")

from . import views
