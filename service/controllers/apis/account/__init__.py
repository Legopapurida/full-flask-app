from flask_smorest import Blueprint


router = Blueprint(
    "account",
    "account",
    url_prefix="/account",
    description="Operations on accounts",
)

from . import routes
