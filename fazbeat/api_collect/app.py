from __future__ import annotations

from typing import Any, Callable

from loguru import logger

from fazbeat.api_collect.heartbeat import Heartbeat
from fazutil.api.wynn.wynn_api import WynnApi
from fazutil.db.fazdb.fazdb_database import FazdbDatabase
from fazutil.properties import Properties
from fazutil.util.logger_setup import LoggerSetup
from fazutil.util.retry_handler import RetryHandler


class App:
    def __init__(self) -> None:
        self._properties = Properties()
        p = self.properties
        p.setup()
        LoggerSetup.setup(
            "logs/fazbeat/api_collect",
            p.API_COLLECT_DISCORD_LOG_WEBHOOK,
            p.ADMIN_DISCORD_ID,
        )

        self._api = WynnApi()
        self._db = FazdbDatabase(
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.FAZDB_DB_NAME,
        )
        self._heartbeat = Heartbeat(self.api, self.db)

        self._register_retry_handler()

    def start(self) -> None:
        logger.info("Starting WynnDb Heartbeat...")
        self.heartbeat.start()

    def stop(self) -> None:
        logger.info("Stopping Heartbeat...")
        self.heartbeat.stop()

    @property
    def api(self) -> WynnApi:
        return self._api

    @property
    def properties(self) -> Properties:
        return self._properties

    @property
    def db(self) -> FazdbDatabase:
        return self._db

    @property
    def heartbeat(self) -> Heartbeat:
        return self._heartbeat

    def _register_retry_handler(self) -> None:
        """Registers retry handler to this appp"""
        register_lambda: Callable[[Callable[..., Any]], None] = (
            lambda func: RetryHandler.register(
                func, self.properties.API_COLLECT_MAX_RETRIES, Exception
            )
        )

        # Register retry handler to database
        repositories = self.db.repositories
        for repo in repositories:
            register_lambda(repo.table_disk_usage)
            register_lambda(repo.create_table)
            register_lambda(repo.insert)
            register_lambda(repo.delete)
            register_lambda(repo.is_exists)
