from datetime import timedelta
from service import BaseConfigs


class ProductionConfigs(BaseConfigs):
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
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)

    class Config:
        env_file = "./environments/.env.production"
