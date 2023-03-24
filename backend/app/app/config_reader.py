from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import Field
from pydantic import PostgresDsn
from pydantic import RedisDsn
from pydantic import validator


class ServiceKey(BaseModel):
    type: str
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str


class Settings(BaseSettings):
    API_V1_URL: str = Field(default="/api/")

    BOT_TOKEN: str
    ID_ADMINS: list[int]

    UPDATE_TIMEOUT: int = Field(default=10)
    TIMEZONE: str = Field(default="Europe/Moscow")

    GSAPI_ID: str
    GSAPI_SERVICE_KEY: ServiceKey

    POSTGRES_USER: str = Field(default="admin")
    POSTGRES_PASSWORD: str = Field(default="qwerty123")
    POSTGRES_DB: str = Field(default="auth_service")
    POSTGRES_HOST: str = Field(default="db")
    POSTGRES_PORT: str = Field(default="5432")

    POSTGRES_URL: Optional[PostgresDsn] = None

    @validator("POSTGRES_URL", pre=True)
    def assemble_postgres_uri(cls, v: Optional[str], values: [str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=f"{values.get('POSTGRES_PORT') or ''}",
        )

    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)

    REDIS_URL: Optional[RedisDsn] = None

    @validator("REDIS_URL", pre=True)
    def assemble_redis_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_HOST"),
            port=str(values.get("REDIS_PORT")),
            path="/0",
        )

    class Config:
        env_file = "./dev.env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "ID_ADMINS":
                return [int(x) for x in raw_val.split(",")]
            return cls.json_loads(raw_val)


config = Settings()
