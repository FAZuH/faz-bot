from abc import ABC
from abc import abstractmethod

from faz.bot.app.discord.embed.builder.embed_builder import EmbedBuilder


class BaseEmbedDirector(ABC):
    """Base class for directing the construction of embeds using an EmbedBuilder.

    Attributes:
        _embed_builder (EmbedBuilder): The builder used to construct embeds.
    """

    def __init__(self, embed_builder: EmbedBuilder) -> None:
        self._embed_builder = embed_builder

    @abstractmethod
    async def setup(self) -> None:
        """Additional async setup for the director.

        Only run once after initialization.
        """

    @property
    def embed_builder(self) -> EmbedBuilder:
        """Embed builder being directed."""
        return self._embed_builder
