from __future__ import annotations

from typing import TYPE_CHECKING

from fazutil.heartbeat.base_heartbeat import BaseHeartbeat

if TYPE_CHECKING:
    from fazcord.app.app import App


class Heartbeat(BaseHeartbeat):
    def __init__(self, app: App) -> None:
        super().__init__("heartbeat_fazcord")
