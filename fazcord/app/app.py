from __future__ import annotations

from contextlib import contextmanager
from threading import Lock
from typing import Generator

from loguru import logger

from fazcord.bot.bot import Bot
from fazcord.heartbeat.heartbeat import Heartbeat
from fazutil.db.fazcord.fazcord_database import FazcordDatabase
from fazutil.db.fazdb.fazdb_database import FazdbDatabase
from fazutil.properties import Properties
from fazutil.util.logger_setup import LoggerSetup


class App:
    def __init__(self) -> None:
        self._locks: dict[str, Lock] = {}

        self._properties = Properties()
        p = self.properties
        p.setup()
        LoggerSetup.setup(
            "logs/fazcord", p.FAZCORD_DISCORD_LOG_WEBHOOK, p.ADMIN_DISCORD_ID
        )

        self._bot = Bot(self)
        self._heartbeat = Heartbeat(self)

    def start(self) -> None:
        logger.info("Starting App")
        self._bot.start()
        self._heartbeat.start()
        logger.success("Started App", discord=True)

    def stop(self) -> None:
        logger.info("Stopping App")
        self._bot.stop()
        self._heartbeat.stop()
        logger.success("Stopped App", discord=True)

    @property
    def properties(self) -> Properties:
        return self._properties

    @contextmanager
    def enter_bot(self) -> Generator[Bot]:
        with self._get_lock("bot"):
            yield self._bot

    def create_fazcord_db(self) -> FazcordDatabase:
        p = self.properties
        return FazcordDatabase(
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.FAZCORD_DB_NAME,
        )

    def create_fazdb_db(self) -> FazdbDatabase:
        p = self.properties
        return FazdbDatabase(
            p.MYSQL_USERNAME,
            p.MYSQL_PASSWORD,
            p.MYSQL_HOST,
            p.MYSQL_PORT,
            p.FAZDB_DB_NAME,
        )

    def _get_lock(self, key: str) -> Lock:
        if key not in self._locks:
            lock = Lock()
            self._locks[key] = lock
        else:
            lock = self._locks[key]
        return lock
