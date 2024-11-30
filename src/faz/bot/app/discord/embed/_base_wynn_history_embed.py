from abc import ABC
from abc import abstractmethod

from faz.bot.app.discord.embed._base_field_pagination_embed import BaseFieldPaginationEmbed


class BaseWynnHistoryEmbed(BaseFieldPaginationEmbed, ABC):
    @abstractmethod
    async def setup(self) -> None: ...

    @abstractmethod
    async def setup_fields(self) -> None: ...
