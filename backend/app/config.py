from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings, validator, EmailStr
import secrets

from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Reports'
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///database.db?check_same_thread=False'
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str = 'abracadabra'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    REPORT_CSV_PANDAS_TYPES: Dict[str, str] = {
        'opco': 'str', 'date': 'date', 'time': 'time', 'rx': 'int', 'tx': 'int'}
    REPORT_MAPPING: Dict[str, str] = {
        'opco': 'opco', 'date': 'date', 'time': 'time', 'rx': 'rx', 'tx': 'tx'}

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:8080']

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
