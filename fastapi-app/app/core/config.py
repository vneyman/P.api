from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "FastAPI App"
    database_url: str | None = Field(default=None, validation_alias="DATABASE_URL")
    postgres_user: str = Field(default="admin", validation_alias="POSTGRES_USER")
    postgres_password: str = Field(default="admin", validation_alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="postgres", validation_alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    postgres_db: str = Field(default="misc", validation_alias="POSTGRES_DB")

    def model_post_init(self, __context: object) -> None:
        if self.database_url is None:
            object.__setattr__(
                self,
                "database_url",
                (
                    f"postgresql://{self.postgres_user}:{self.postgres_password}"
                    f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
                ),
            )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
