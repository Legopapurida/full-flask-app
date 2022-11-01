from datetime import datetime, timezone
from flask import Request
from flask import Flask
from flask import Response
from flask import session
from flask import g
from flask_smorest import abort
from service import Application as root
from .loaders import UserLoader
from .loaders import UserModel


class BaseMiddleware:
    def before_request(self, request: Request = None) -> None:
        pass

    def after_request(self, response: Response) -> Response:
        return response


class AuthMiddleware(BaseMiddleware):
    def __init__(self, app: Flask):
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def data_decoder(self, data: bytes) -> dict:
        """``decode`` the returned data from redis and convert it to `dict`

        Args:
            data (bytes): data body

        Returns:
            dict: data `bytes` to `dict`
        """
        return dict(eval(data.decode().replace('"', "'")))

    def before_request(self) -> None:
        aid = session.get("aid")
        g.user = None
        if aid:
            session_token = root.redis.client.hget("users", aid)
            if session_token:
                tokens = self.data_decoder(session_token)
                try:
                    data = root.jwt.decode(tokens["access_token"])
                except:
                    try:
                        data = root.jwt.decode(tokens["refresh_token"])
                    except Exception:
                        abort(403)

                user = UserModel(
                    id=data["id"],
                    username=data["username"],
                    email=data["email"],
                    last_name=data["last_name"],
                    first_name=data["first_name"],
                )
                g.user = user

    def after_request(self, response: Response) -> Response:
        try:
            aid = session.get("aid")
            if aid:
                session_token = root.redis.client.hget("users", aid)
                if session:
                    tokens = self.data_decoder(session_token)
                    identity = root.jwt.decode(tokens["refresh_token"])
                    exp_timestamp = identity["exp"]
                    now = datetime.now(timezone.utc)
                    target_timestamp = datetime.timestamp(
                        now + root.configs.JWT_REFRESH_TOKEN_EXPIRES
                    )
                    if target_timestamp > exp_timestamp:
                        tokens["access_token"] = root.jwt.generate_access_token(
                            identity
                        )
                        tokens = root.redis.client.hset("users", aid, str(tokens))
                    return response
        except:
            pass
        return response
