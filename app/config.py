from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    test_database_url: str | None = None

    @property
    def sqlalchemy_url(self) -> str:
        return self.database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    @property
    def sqlalchemy_test_url(self) -> str | None:
        if self.test_database_url is None:
            return None
        return self.test_database_url.replace("postgresql://", "postgresql+psycopg://", 1)


settings = Settings()