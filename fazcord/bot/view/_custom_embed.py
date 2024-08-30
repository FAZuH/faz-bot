from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Self, Union

from nextcord import Colour, Embed, Interaction
from nextcord.types.embed import EmbedType


class CustomEmbed(Embed):

    def __init__(
        self,
        interaction: Interaction[Any],
        *,
        thumbnail_url: Optional[str] = None,
        colour: Optional[Union[int, Colour]] = None,
        color: Optional[Union[int, Colour]] = None,
        title: Optional[Any] = None,
        type: EmbedType = "rich",
        url: Optional[Any] = None,
        description: Optional[Any] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        super().__init__(
            colour=colour,
            color=color,
            title=title,
            type=type,
            url=url,
            description=description,
            timestamp=timestamp,
        )
        self._memento = {
            "interaction": interaction,
            "thumbnail_url": thumbnail_url,
            "colour": colour,
            "color": color,
            "title": title,
            "type": type,
            "url": url,
            "description": description,
            "timestamp": timestamp,
        }
        self._interaction = interaction

        self.set_thumbnail(thumbnail_url)
        self.add_author()

    def get_base(self) -> Self:
        """Returns a new instance of CustomEmbed with the initial state."""
        return self.__class__(**self._memento)

    def finalize(self) -> None:
        """Do setup that needs to be run at the end of preparation of this object."""
        self.add_timestamp_field()

    def add_author(self) -> None:
        """Adds author to this embed."""
        user = self.interaction.user
        assert user, "User is None. Who is calling this?"
        self.set_author(
            name=user.display_name,
            icon_url=user.display_avatar.url,
        )

    def add_timestamp_field(self) -> None:
        """Adds a timestamp field to this embed."""
        timestamp = self._interaction.created_at.timestamp()
        self.add_field(name="Timestamp", value=f"<t:{int(timestamp)}:F>", inline=False)

    @property
    def interaction(self) -> Interaction[Any]:
        """Returns the interaction associated with this embed."""
        return self._interaction
