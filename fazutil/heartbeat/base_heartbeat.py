from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING

from loguru import logger

from fazutil.heartbeat._heartbeat_task import HeartbeatTask

if TYPE_CHECKING:
    from fazutil.heartbeat.task.itask import ITask


class BaseHeartbeat(Thread):

    def __init__(self, name: str | None = None) -> None:
        super().__init__(target=self.run, daemon=True, name=name)
        self._tasks: list[HeartbeatTask] = []

    def start(self) -> None:
        logger.info("Starting Heartbeat")
        for task in self._tasks:
            task.start()
        logger.success("Started Heartbeat")

    def stop(self) -> None:
        logger.info("Stopping Heartbeat")
        for task in self._tasks:
            task.cancel()
        logger.success("Stopped Heartbeat")

    def _add_task(self, task: ITask) -> None:
        self._tasks.append(HeartbeatTask(task))
