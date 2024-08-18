from __future__ import annotations
from typing import TYPE_CHECKING

from .task import RequestQueue, ResponseQueue, TaskApiRequest, TaskDbInsert
from fazutil.heartbeat import BaseHeartbeat

if TYPE_CHECKING:
    from fazutil.api import WynnApi
    from fazutil.db import FazdbDatabase


class Heartbeat(BaseHeartbeat):

    def __init__(self, api: WynnApi, db: FazdbDatabase) -> None:
        super().__init__()

        request_queue = RequestQueue()
        response_queue = ResponseQueue()
        api_request = TaskApiRequest(api, request_queue, response_queue)
        db_insert = TaskDbInsert(api, db, request_queue, response_queue)

        self._add_task(api_request)
        self._add_task(db_insert)
