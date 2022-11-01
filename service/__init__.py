from datetime import timedelta
from typing import Any, Protocol
from flask import Flask
from flask_smorest import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .extensions.jwt.manager import JwtManager
from .extensions import MongoDB
from .extensions import RedisDB
from .extensions import PostgresDB
from pydantic import BaseSettings


class __ApplicationFunctionalities(Protocol):
    def install_app(self) -> None:
        ...

    def install_context_processors(self) -> None:
        ...

    def install_event_handlers(self) -> None:
        ...

    def install_extensions(self) -> None:
        ...

    def install_middlewares(self) -> None:
        ...

    def install_blueprints(self) -> None:
        ...

    def install_commands(self) -> None:
        ...

    def install_exceptions(self) -> None:
        ...

    def create_app(self) -> Any:
        ...


class BaseConfigs(BaseSettings):
    SECRET_KEY: str
    API_TITLE: str
    API_VERSION: str
    OPENAPI_VERSION: str
    OPENAPI_JSON_PATH: str
    OPENAPI_URL_PREFIX: str
    OPENAPI_SWAGGER_UI_PATH: str
    OPENAPI_SWAGGER_UI_URL: str
    JWT_SECRET_KEY: str
    MONGO_DATABASE_NAME: str
    MONGO_DATABASE_URI: str
    SQL_DATABASE_URI: str
    REDIS_DATABASE_URI: str
    JWT_ACCESS_TOKEN_EXPIRES: timedelta
    JWT_REFRESH_TOKEN_EXPIRES: timedelta


class Application:
    app: Flask = None
    configs: BaseConfigs = None
    api: Api = None
    jwt: JwtManager = None
    mongo: MongoDB = None
    redis: RedisDB = None
    postgres: PostgresDB = None
    limiter: Limiter = None


class CreateProductionApplication(Application, __ApplicationFunctionalities):
    # Facade Pattern

    def __init__(self, configs: BaseConfigs) -> None:
        self.configs = Application.configs = configs

    def install_app(self) -> None:
        self.app = Application.app = Flask(__name__)
        self.app.config.from_object(self.configs)

    def install_middlewares(self) -> None:
        from .core.middleware import AuthMiddleware
        from flask_cors import CORS

        AuthMiddleware(app=self.app)
        CORS(app=self.app)

    def install_event_handlers(self) -> None:
        @self.app.before_first_request
        def start_up():
            self.app.logger.info("Server is ready")
            if self.redis.client.ping():
                self.app.logger.info("Redis is ready")
            try:
                self.mongo.database.client.server_info()
                self.app.logger.info("Mongo is ready")
            except Exception as error:
                self.app.logger.error(error)

    def install_extensions(self) -> None:
        from .extensions.base import ExtensionInstaller as CustomExtensionsInstaller

        self.api = Application.api = Api(app=self.app)
        self.jwt = Application.jwt = JwtManager(
            self.configs.JWT_SECRET_KEY,
            self.configs.JWT_ACCESS_TOKEN_EXPIRES,
            self.configs.JWT_REFRESH_TOKEN_EXPIRES,
        )
        self.mongo = Application.mongo = MongoDB(self.configs.dict())
        self.postgres = Application.postgres = PostgresDB(self.configs.dict())
        self.redis = Application.redis = RedisDB(self.configs.dict())
        self.limiter = Application.limiter = Limiter(
            app=self.app,
            key_func=get_remote_address,
            storage_uri=self.configs.REDIS_DATABASE_URI,
        )
        installer = CustomExtensionsInstaller(
            self.mongo,
            self.redis,
            self.postgres,
        )
        installer.install_extensions()

    def install_blueprints(self) -> None:
        from .controllers.apis import auth
        from .controllers.apis import account
        from .controllers import frontend

        self.api.register_blueprint(auth.router)
        self.api.register_blueprint(account.router)
        self.app.register_blueprint(frontend.router)

    def install_commands(self) -> None:
        from .command import db

        self.app.cli.add_command(db.cli)

    def install_context_processors(self) -> None:
        from .core import context_processor

        self.app.context_processor(context_processor.current_user)

    def create_app(self) -> Flask:
        self.install_app()
        self.install_extensions()
        self.install_blueprints()
        self.install_middlewares()
        self.install_exceptions()
        self.install_event_handlers()
        self.install_context_processors()
        self.install_commands()

        return self.app
