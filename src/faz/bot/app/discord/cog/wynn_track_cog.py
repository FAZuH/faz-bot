from typing import Any, Iterable, Literal, override

from nextcord import Interaction
from nextcord import slash_command

from faz.bot.app.discord.bot.errors import InvalidActionException
from faz.bot.app.discord.bot.errors import InvalidArgumentException
from faz.bot.app.discord.cog._base_cog import CogBase


class WynnTrackCog(CogBase):
    @override
    def _setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        super()._setup(whitelisted_guild_ids)
        self.track.add_check(self._bot.checks.is_guild_admin)
        self.track_admin.add_check(self._bot.checks.is_admin)
        self.track_admin.add_guild_rollout(self._bot.app.properties.DEV_SERVER_ID)
        self._bot.client.add_application_command(self.track_admin, overwrite=True, use_rollout=True)

    @slash_command()
    async def track(self, intr: Interaction[Any]) -> None:
        """Commands to manage and view Wynncraft trackers."""

    @slash_command()
    async def track_admin(self, intr: Interaction[Any]) -> None:
        """Contains administrative commands for managing Wynncraft trackers."""

    @track_admin.subcommand(name="toggle")
    async def toggle(self, intr: Interaction[Any], channel_id: str) -> None:
        """(dev only) Toggles a track entry on any channel_id."""
        db = self._bot.fazcord_db
        channel = await self._utils.must_get_channel(channel_id)
        track_entry = await db.track_entry.toggle(channel.id)
        await self._respond_successful(
            intr,
            f"Toggled track entry on channel `{channel.id}` (`{channel.name}`) to {track_entry}",  # type: ignore
        )

    @track.subcommand()
    async def show(self, intr: Interaction[Any]) -> None:
        """Shows all Wynncraft trackers on this server."""
        db = self._bot.fazcord_db
        guild_id = intr.guild.id  # type: ignore
        track_entries = await db.track_entry.select_by_guild_id(guild_id)
        if len(track_entries) == 0:
            await self._respond_successful(
                intr, "This server does not have any Wynncraft trackers registred"
            )
        else:
            responses = []
            for entry in track_entries:
                await entry.awaitable_attrs.channel
                responses.append(
                    f"- `{entry.channel_id} ({entry.channel.channel_name})`: {entry.type}"
                )
                if entry.type in {"GUILD", "ONLINE"}:
                    await entry.awaitable_attrs.associations
                    subresponses = []
                    for value in entry.associations:
                        subresponses.append(f"\t- `{value.associated_value}`")
                    subresponse = "\n".join(subresponses)
                    responses.append(subresponse)
            response = "\n".join(responses)
            await self._respond_successful(intr, response)

    @track.subcommand(name="toggle")
    async def toggle_(self, intr: Interaction[Any], channel_id: str) -> None:
        """Toggles a track entry on/off.

        Args:
            channel_id (str): The ID of the channel to toggle tracking for.
        """
        db = self._bot.fazcord_db
        channel = await self._utils.must_get_channel(channel_id)
        track_entry = await db.track_entry.toggle(channel.id)
        await self._respond_successful(
            intr,
            f"Toggled track entry on channel `{channel.id} ({channel.name})` to {track_entry}",  # type: ignore
        )

    @track.subcommand()
    async def remove(self, intr: Interaction[Any], channel_id: str) -> None:
        """Removes a track entry.

        Args:
            channel_id (str): The ID of the channel to remove the track entry from.
        """
        db = self._bot.fazcord_db
        channel = await self._utils.must_get_channel(channel_id)
        await db.track_entry.delete(channel.id)
        await self._respond_successful(
            intr,
            f"Removed track entry on channel `{channel.id} ({channel.name})`",  # type: ignore
        )

    @track.subcommand()
    async def guild(self, intr: Interaction[Any], channel_id: str, guild: str) -> None:
        """Adds a guild-wide tracker.

        Args:
            channel_id (str): The ID of the channel to add the tracking entry to.
            guild (str): The name of the guild to track.
        """
        await self._add_track_entry(intr, channel_id, "GUILD", guild)

    @track.subcommand()
    async def hunted(self, intr: Interaction[Any], channel_id: str) -> None:
        """Adds a tracker for hunted players.

        Args:
            channel_id (str): The ID of the channel to add the tracking entry to.
        """
        await self._add_track_entry(intr, channel_id, "HUNTED")

    @track.subcommand()
    async def online(self, intr: Interaction[Any], channel_id: str, user: str) -> None:
        """Adds a tracker for online players.

        Args:
            channel_id (str): The ID of the channel to add the tracking entry to.
            user (str): The user to track online status for.
        """
        await self._add_track_entry(intr, channel_id, "ONLINE", user)

    @track.subcommand()
    async def player(self, intr: Interaction[Any], channel_id: str, user: str) -> None:
        """Adds a tracker for a specific player.

        Args:
            channel_id (str): The ID of the channel to add the tracker to.
            user (str): The user to track.
        """
        await self._add_track_entry(intr, channel_id, "PLAYER", user)

    @track.subcommand()
    async def staff(self, intr: Interaction[Any], channel_id: str) -> None:
        """Adds a tracker for staff members.

        Args:
            channel_id (str): The ID of the channel to add the tracker to.
        """
        await self._add_track_entry(intr, channel_id, "STAFF")

    async def _add_track_entry(
        self,
        intr: Interaction[Any],
        channel_id: str,
        type: Literal["GUILD", "HUNTED", "ONLINE", "PLAYER", "STAFF"],
        value: str | None = None,
    ) -> None:
        """Adds or updates a track entry for a specific channel based on the provided type and value.

        This method handles adding new tracking entries or updating existing ones for a specified
        channel in a Discord server. It also allows the association of additional values for types
        "PLAYER" and "GUILD" with the track entry. If the specified value already exists, it removes the
        association; otherwise, it creates a new association. The method also ensures that a track
        entry is removed if it has no more associated values after deletion.

        Args:
            intr (Interaction): The interaction object containing the context of the command invocation.
            channel_id (str): The ID of the channel where the track entry is to be added or modified.
            type (Literal["GUILD", "HUNTED", "ONLINE", "PLAYER", "STAFF"]): The type of tracking entry
                to be added or modified. Only "GUILD" and "ONLINE" types can have additional associated values.
            value (str, optional): The optional value to associate with the track entry (e.g., a guild name
                or player UUID). Required for "GUILD" and "ONLINE" types.

        Raises:
            BadArgument: If a guild or player cannot be fetched using the provided `value`, or if
                an invalid track entry type is provided for editing.
        """
        db = self._bot.fazcord_db
        track_repo = db.track_entry
        track_value_repo = db.track_entry_association
        channel = await self._utils.must_get_channel(channel_id)
        assert intr.user

        async with db.enter_async_session() as ses:
            await self._utils.add_to_db(intr, channel, ses)
            track_entry = await track_repo.select_by_channel_id(channel.id, session=ses)

            if track_entry is None:
                # NOTE: Add track entry
                track_entry = track_repo.model(
                    channel_id=channel.id,
                    created_by=intr.user.id,
                    enabled=True,
                    type=type,
                )
                await track_repo.insert(track_entry, session=ses)

                await self._respond_successful(
                    intr,
                    f"Added `{type}` track entry on channel `{channel.id} ({channel.name})`",  # type: ignore
                )
                return

            if type == "GUILD":
                assert value
                guild = await self._bot.fazwynn_db.guild_info.get_guild(value)
                if not guild:
                    raise InvalidArgumentException(
                        f"Guild {value} does not exist in faz-bot's database"
                    )
                uuid = guild.uuid

            elif type == "ONLINE":
                assert value
                player = await self._bot.fazwynn_db.player_info.get_player(value)
                if not player:
                    raise InvalidArgumentException(
                        f"Player {value} does not exist in faz-bot's database"
                    )
                uuid = player.uuid
            else:
                raise InvalidActionException(
                    "Tracker that is not of type `guild` or `online` cannot be edited. "
                    f"Remove with `/remove {channel_id}`."
                )

            # NOTE: Toggle
            await track_entry.awaitable_attrs.associations
            associations_size = len(track_entry.associations)
            for val in track_entry.associations:
                if val.associated_value == uuid:
                    # NOTE: Value exists. Remove the value
                    await ses.delete(val)
                    if associations_size == 1:
                        # NOTE: The deleted value was the latest value associated with the track entry
                        await ses.delete(track_entry)
                        await self._respond_successful(
                            intr,
                            f"Removed track entry on channel `{channel.id} ({channel.name})`",  # type: ignore
                        )
                        return
                    await self._respond_successful(
                        intr,
                        f"Removed {type.lower()} `{value}` from `{type}` track entry on channel `{channel.id} ({channel.name})`",  # type: ignore
                    )
                    return

            # NOTE: Value is new. Add the value
            track_value = track_value_repo.model(
                track_entry_id=track_entry.id, associated_value=uuid
            )

            await track_value_repo.insert(track_value, session=ses)
            await self._respond_successful(
                intr,
                f"Added {type.lower()} `{value}` to `{type}` track entry on channel `{channel.id} ({channel.name})`",  # type: ignore
            )
