#app/core/config.py

from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseModel):
    driver: str = "asyncpg"
    user: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    host: str = os.getenv("POSTGRES_HOST", "localhost")
    port: int = int(os.getenv("POSTGRES_PORT", 5432))
    database: str = os.getenv("POSTGRES_DB", "myshop_db")
    echo: bool = False  # вывод SQL-запросов в консоль

    @property
    def url(self) -> str:
        """Собирает полный URL для SQLAlchemy Async Engine"""
        return f"postgresql+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    # refresh_token_expire_minutes: int = 60 * 24 * 30
    # access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()

    # db_echo: bool = True


settings = Settings()
