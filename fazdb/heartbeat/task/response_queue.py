from __future__ import annotations
from threading import Lock
from typing import Any, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from fazutil.api import BaseResponse

    type Resp = BaseResponse[Any, Any]


class ResponseQueue:

    def __init__(self):
        self._list: list[Resp] = []
        self._lock = Lock()

    def get(self) -> list[Resp]:
        with self._lock:
            ret = self._list
            self._list = []
        return ret

    def put(self, responses: Iterable[Resp]) -> None:
        with self._lock:
            self._list.extend(responses)
