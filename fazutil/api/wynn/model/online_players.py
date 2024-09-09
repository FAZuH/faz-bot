from typing import Any, Generator

from fazutil.api.wynn.model.field.username_or_uuid_field import UsernameOrUuidField


class OnlinePlayers:

    __slots__ = ("_raw", "_total", "_players")

    def __init__(self, raw: dict[str, Any]) -> None:
        self._raw = raw
        self._total = raw["total"]
        self._players = {
            UsernameOrUuidField(usernameoruuid): server
            for usernameoruuid, server in raw["players"].items()
            if server is not None
        }

    def iter_players(self) -> Generator[tuple[UsernameOrUuidField, str], Any, None]:
        yield from self._players.items()

    @property
    def raw(self) -> dict[str, Any]:
        return self._raw

    @property
    def total(self) -> int:
        return self._total

    @property
    def players(self) -> dict[UsernameOrUuidField, str]:
        return self._players
