from __future__ import annotations

from typing import Any, Self, TYPE_CHECKING

from nextcord import Embed

if TYPE_CHECKING:
    from nextcord import Colour
    from nextcord import Interaction


class EmbedBuilder:
    def __init__(self, interaction: Interaction[Any] | None = None, initial_embed: Embed | None = None) -> None:
        self._initial_embed = self._embed = initial_embed or Embed()
        self._interaction = interaction

    def add_field(self, name: str, value: str, inline: bool = False) -> Self:
        self._embed.add_field(name=name, value=value, inline=inline)
        return self

    def set_colour(self, colour: Colour | int) -> Self:
        self._embed.colour = colour
        return self

    def set_footer(self, text: str | None = None, icon_url: str | None = None) -> Self:
        self._embed.set_footer(text=text, icon_url=icon_url)
        return self

    def set_interaction(self, interaction: Interaction[Any]) -> Self:
        self._interaction = interaction
        return self

    def set_thumbnail(self, url: str) -> Self:
        self._embed.set_thumbnail(url)
        return self

    def set_title(self, title: str) -> Self:
        self._embed.title = title
        return self

    def set_description(self, description: str) -> Self:
        self._embed.description = description
        return self

    def build(self) -> Embed:
        """Finalize the embed construction, and return the finished product.

        Returns:
            Embed: The embed object.
        """
        self._add_author()
        return self._embed

    def get_embed(self) -> Embed:
        """Get the embed without finalizing it.

        Returns:
            Embed: The embed object.
        """
        return self._embed

    def reset_embed(self) -> Self:
        """Resets the embed to its initial state."""
        self._embed = self._initial_embed.copy()
        return self

    def set_builder_initial_embed(self, embed: Embed) -> Self:
        """Sets the initial embed state for this builder.

        Args:
            embed (Embed): The embed to set.

        Returns:
            Self: The builder instance.
        """
        self._initial_embed = embed
        return self

    def _add_author(self) -> Self:
        """Adds author to this embed."""
        user = self.interaction.user
        assert user, "User is None. Who is calling this command?"
        self._embed.set_author(
            name=user.display_name,
            icon_url=user.display_avatar.url,
        )
        self._embed.timestamp = self.interaction.created_at
        return self

    @property
    def interaction(self) -> Interaction[Any]:
        """Returns the interaction associated with this embed.

        Raises:
            ValueError: If interaction is not set.
        """
        ret = self._interaction
        if ret is None:
            raise ValueError("Interaction is not set.")
        return ret
