from flask_smorest import Blueprint


router = Blueprint(
    "auth",
    "auth",
    url_prefix="/auth",
    description="Operations on authentication",
)

from . import routes
