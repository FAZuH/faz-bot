from __future__ import annotations
from typing import TYPE_CHECKING

from fazutil.heartbeat import BaseHeartbeat

if TYPE_CHECKING:
    from fazbot.app import App


class Heartbeat(BaseHeartbeat):

    def __init__(self, app: App) -> None:
        super().__init__()
