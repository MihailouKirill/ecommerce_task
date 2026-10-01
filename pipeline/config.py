from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "app_settings"]


class Settings(BaseSettings):
    """
    Class with settings configuration

    Reads settings from env file +
    adjusts the batch size
    """

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    batch_size: int

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
    )


# Loading settings for import
app_settings = Settings()
