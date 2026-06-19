# app/core/config.py

from pathlib import Path

from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings

import os

BASE_DIR = Path(__file__).parent.parent


# -------------------------
# DATABASE
# -------------------------
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
        return (
            f"postgresql+{self.driver}://"
            f"{self.user}:{self.password}@"
            f"{self.host}:{self.port}/"
            f"{self.database}"
        )


# -------------------------
# JWT AUTH
# -------------------------
class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"

    algorithm: str = "RS256"

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


# -------------------------
# SMTP
# -------------------------
class SmtpConfig(BaseModel):
    host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port: int = int(os.getenv("SMTP_PORT", 587))

    user: str | None = os.getenv("SMTP_USER") or None
    password: str | None = os.getenv("SMTP_PASSWORD") or None

    from_email: EmailStr | None = os.getenv("SMTP_FROM_EMAIL")

    start_tls: bool = True
    use_tls: bool = False

    def get_from(self) -> EmailStr:
        return self.from_email or self.user  # type: ignore


# -------------------------
# YOOKASSA
# -------------------------
class YookassaConfig(BaseModel):
    shop_id: str | None = os.getenv("YOOKASSA_SHOP_ID")
    secret_key: str | None = os.getenv("YOOKASSA_SECRET_KEY")

    def validate(self) -> None:
        """
        Проверка обязательных параметров при старте приложения
        """
        if not self.shop_id or not self.secret_key:
            raise ValueError("YOOKASSA_SHOP_ID or YOOKASSA_SECRET_KEY is missing")


# -------------------------
# SETTINGS ROOT
# -------------------------
class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    smtp: SmtpConfig = SmtpConfig()
    yookassa: YookassaConfig = YookassaConfig()

    # db_echo: bool = True


# single instance
settings = Settings()
