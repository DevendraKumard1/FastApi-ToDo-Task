from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool
    
    HOST: str
    PORT: int

    MYSQLUSER: str
    MYSQLPASSWORD: str
    MYSQLHOST: str
    MYSQLPORT: int
    MYSQLDATABASE: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_URL: str | None = None

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

@lru_cache()
def get_settings():
    return Settings()
