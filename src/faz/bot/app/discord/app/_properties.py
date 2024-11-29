import os
from typing import Callable

from dotenv import load_dotenv

from faz.bot.app.discord import __version__


class Properties:
    # Application constants
    AUTHOR = "FAZuH"
    VERSION = __version__

    # .env
    DISCORD_BOT_TOKEN: str
    DEV_DISCORD_ID: int
    DEV_SERVER_ID: int
    FAZCORD_DISCORD_LOG_WEBHOOK: str
    FAZCORD_DISCORD_STATUS_WEBHOOK: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_FAZWYNN_DATABASE: str
    MYSQL_FAZCORD_DATABASE: str
    FAZCORD_MAX_RETRIES: int

    # # Additional application property classes
    # ASSET: Asset

    @classmethod
    def setup(cls) -> None:
        """Bootstraps application properties."""
        cls._read_env()
        # cls.ASSET = Asset(cls.ASSET_DIR)
        # cls.ASSET.read_all()

    @classmethod
    def _read_env(cls) -> None:
        load_dotenv()
        cls.DISCORD_BOT_TOKEN = cls._must_get_env("DISCORD_BOT_TOKEN")
        cls.DEV_DISCORD_ID = cls._must_get_env("DEV_DISCORD_ID", int)
        cls.DEV_SERVER_ID = cls._must_get_env("DEV_SERVER_ID", int)
        cls.FAZCORD_DISCORD_LOG_WEBHOOK = cls._must_get_env("FAZCORD_DISCORD_LOG_WEBHOOK")
        cls.FAZCORD_DISCORD_STATUS_WEBHOOK = cls._must_get_env("FAZCORD_DISCORD_STATUS_WEBHOOK")
        cls.FAZCORD_MAX_RETRIES = cls._must_get_env("FAZCORD_MAX_RETRIES", int)
        cls.MYSQL_HOST = cls._must_get_env("MYSQL_HOST")
        cls.MYSQL_PORT = cls._must_get_env("MYSQL_PORT", int)
        cls.MYSQL_USER = cls._must_get_env("MYSQL_USER")
        cls.MYSQL_PASSWORD = cls._must_get_env("MYSQL_PASSWORD")
        cls.MYSQL_FAZCORD_DATABASE = cls._must_get_env("MYSQL_FAZCORD_DATABASE")
        cls.MYSQL_FAZWYNN_DATABASE = cls._must_get_env("MYSQL_FAZWYNN_DATABASE")

    @staticmethod
    def _must_get_env[T](key: str, type_strategy: Callable[[str], T] = str) -> T:
        try:
            env = os.getenv(key)
            return type_strategy(env)  # type: ignore
        except ValueError as exc:
            raise ValueError(
                f"Failed parsing environment variable {key} into type {type_strategy}"
            ) from exc
