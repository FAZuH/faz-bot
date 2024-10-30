from __future__ import annotations

from typing import TYPE_CHECKING

from fazbeat.fazcollect.task.request_queue import RequestQueue
from fazbeat.fazcollect.task.response_queue import ResponseQueue
from fazbeat.fazcollect.task.task_api_request import TaskApiRequest
from fazbeat.fazcollect.task.task_db_insert import TaskDbInsert
from fazutil.heartbeat.base_heartbeat import BaseHeartbeat

if TYPE_CHECKING:
    from fazutil.api.wynn.wynn_api import WynnApi
    from fazutil.db.fazwynn.fazwynn_database import FazwynnDatabase


class Heartbeat(BaseHeartbeat):
    def __init__(self, api: WynnApi, db: FazwynnDatabase) -> None:
        super().__init__("heartbeat_fazcollect")

        request_queue = RequestQueue()
        response_queue = ResponseQueue()
        api_request = TaskApiRequest(api, request_queue, response_queue)
        db_insert = TaskDbInsert(api, db, request_queue, response_queue)

        self._add_task(api_request)
        self._add_task(db_insert)
