from typing import Any, Dict, Optional

from pydantic import Field, PositiveInt, validator, AnyUrl, BaseSettings


class AsyncDsn(AnyUrl):
    allowed_schemes = {'postgresql+asyncpg'}
    user_required = True


class DBEnv(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"
        case_sensitive = True

    SCHEMA: str = 'postgresql+asyncpg'
    POSTGRES_HOST: str = Field(default="0.0.0.0")

    POSTGRES_USER: str = Field(default="test_user")
    POSTGRES_PASSWORD: str = Field(default="test_password")

    POSTGRES_DB: str = Field(default="dev_db")
    POSTGRES_PORT: PositiveInt = Field(default=5432)
    POSTGRES_URL: Optional[AsyncDsn] = Field(default=None)

    POSTGRES_TEST_DB: str = Field(default="test_db")
    POSTGRES_TEST_PORT: PositiveInt = Field(default=5432)
    POSTGRES_TEST_URL: Optional[AsyncDsn] = Field(default=None)

    @classmethod
    def _create_db_url(cls, values: Dict[str, Any], test: bool = False) -> str:
        port_field = "POSTGRES_PORT" if not test else "POSTGRES_TEST_PORT"
        db_field = "POSTGRES_DB" if not test else "POSTGRES_TEST_DB"

        return AsyncDsn.build(
            scheme=values.get("SCHEMA"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=str(values.get(port_field)),
            path=f"/{values.get(db_field)}",
        )

    @validator("POSTGRES_URL", pre=True)
    def create_db_url(cls, _: Optional[str], values: Dict[str, Any]) -> str:
        return cls._create_db_url(values)

    @validator("POSTGRES_TEST_URL", pre=True)
    def create_test_db_url(cls, _: Optional[str], values: Dict[str, Any]) -> str:
        return cls._create_db_url(values, test=True)
