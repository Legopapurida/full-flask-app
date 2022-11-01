from functools import wraps
from typing import Any
from flask import g
from flask_smorest import abort


class BasePermissions:
    def has_permission(self) -> bool:
        return True

    def raise_error(self):
        raise NotImplementedError

    def __call__(self, func) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.has_permission():
                return func(*args, **kwargs)
            self.raise_error()

        return wrapper


class IsAuthenticated(BasePermissions):
    def has_permission(self) -> bool:
        if g.user:
            return True
        return False

    def raise_error(self):
        abort(401)
