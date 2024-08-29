from typing import Any

from fazutil.api.base_response import BaseResponse
from fazutil.api.wynn.model.headers import Headers
from fazutil.api.wynn.model.online_players import OnlinePlayers


class OnlinePlayersResponse(BaseResponse[OnlinePlayers, Headers]):

    def __init__(self, body: dict[str, Any], headers: dict[str, Any]) -> None:
        super().__init__(OnlinePlayers(body), Headers(headers))
