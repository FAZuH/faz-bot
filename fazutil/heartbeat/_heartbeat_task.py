from __future__ import annotations

from threading import Timer
from time import perf_counter
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from fazutil.heartbeat.task.itask import ITask


class HeartbeatTask:
    def __init__(self, task: ITask) -> None:
        self._task = task
        self._timer = Timer(self.task.first_delay, self._run)
        self._set_timer_name(self._timer)

    def start(self) -> None:
        self._task.setup()
        self._timer.start()

    def cancel(self) -> None:
        self._timer.cancel()
        self._task.teardown()

    @property
    def task(self) -> ITask:
        return self._task

    def _run(self) -> None:
        t1 = perf_counter()
        self._task.run()
        logger.success(f"Task {self.task.name} took {perf_counter() - t1:.2f} seconds")
        self._reschedule()

    def _reschedule(self) -> None:
        self._timer = Timer(self.task.interval, self._run)
        self._set_timer_name(self._timer)
        self._timer.start()

    def _set_timer_name(self, timer: Timer) -> None:
        timer.name = f"HeartbeatTask_{self._task.name}"
