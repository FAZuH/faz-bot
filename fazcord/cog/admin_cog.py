from __future__ import annotations

import subprocess
from typing import Any, Iterable, override

import nextcord
from nextcord import Interaction

from fazcord.bot._utils import Utils
from fazcord.cog._base_cog import CogBase
from fazcord.bot.errors import ApplicationException, InvalidActionException


class AdminCog(CogBase):
    @override
    def _setup(self, whitelisted_guild_ids: Iterable[int]) -> None:
        for app_cmd in self.application_commands:
            app_cmd.add_guild_rollout(self._bot.app.properties.DEV_SERVER_ID)
            self._bot.client.add_application_command(
                app_cmd, overwrite=True, use_rollout=True
            )

    @override
    def cog_application_command_check(self, intr: Interaction[Any]):  # type: ignore
        return self._bot.checks.is_admin(intr)

    @nextcord.slash_command(name="admin", description="Admin commands.")
    async def admin(self, intr: Interaction[Any]) -> None: ...

    @admin.subcommand(name="ban")
    async def ban(
        self,
        intr: Interaction[Any],
        user_id: str,
        reason: str | None = None,
        until: str | None = None,
    ) -> None:
        """(dev only) Bans an user from using the bot.

        Parameters
        ----------
        user_id : str
            The user ID to ban.
        reason : str, optional
            Reason of ban, by default ''
        until : str | None, optional
            Time when the user will be unbanned, by default None
        """
        user = await self._bot.utils.must_get_user(user_id)

        async with self._enter_botdb_session() as (db, s):
            repo = db.whitelist_group

            if await repo.is_banned_user(user.id, session=s):
                raise InvalidActionException(
                    f"User `{user.name} ({user.id})` is already banned"
                )

            await repo.ban_user(
                user.id,
                reason,
                Utils.must_parse_date_string(until) if until else None,
                session=s,
            )

        await self._respond_successful(intr, f"Banned user `{user.name} ({user.id})`")

    @admin.subcommand(name="unban")
    async def unban(self, intr: Interaction[Any], user_id: str) -> None:
        """(dev only) Unbans an user from using the bot.

        Parameters
        ----------
        user_id : str
            The user ID to unban.
        """
        user = await self._utils.must_get_user(user_id)

        async with self._enter_botdb_session() as (db, s):
            repo = db.whitelist_group

            if not await repo.is_banned_user(user.id, session=s):
                raise InvalidActionException(
                    f"User `{user.name} ({user.id})` is not banned"
                )

            await repo.unban_user(user.id, session=s)

        await self._respond_successful(
            intr, f"Unbanned user `{user.name} ({user.id}).`"
        )

    @admin.subcommand(name="echo")
    async def echo(self, intr: Interaction[Any], message: str) -> None:
        """(dev only) Echoes a message.

        Parameters
        ----------
        message : str
            The message to echo.
        """
        await intr.send(message)

    @admin.subcommand(name="send")
    async def send(self, intr: Interaction[Any], channel_id: str, message: str) -> None:
        """(dev only) Unbans an user from using the bot.

        Parameters
        ----------
        channel_id : str
            The channel ID to send the message.
        message : str
            Message to send.
        """
        channel = await self._utils.must_get_channel(channel_id)

        if not self._is_channel_sendable(channel):
            raise ApplicationException(
                f"Channel of type `{type(channel)}` does not support sending messages"
            )

        try:
            await channel.send(message)  # type: ignore
        except nextcord.DiscordException as exc:
            raise ApplicationException(f"Failed sending message: {exc}") from exc

        await self._respond_successful(
            intr, f"Sent message on channel `{channel.name} ({channel.id})`"  # type: ignore
        )  # type: ignore

    @admin.subcommand(name="sync_guild")
    async def sync_guild(self, intr: Interaction[Any], guild_id: str) -> None:
        """(dev only) Syncs app commands for a specific guild.

        Parameters
        ----------
        guild_id : str
            The guild ID to sync app commands to.
        """
        await intr.response.defer()
        guild = await self._utils.must_get_guild(guild_id)

        await self._bot.client.sync_application_commands(guild_id=guild.id)

        synced_app_cmds = 0
        for app_cmd in self._bot.client.get_all_application_commands():
            if guild.id in app_cmd.guild_ids:
                synced_app_cmds += 1

        await self._respond_successful(
            intr,
            f"Synchronized {synced_app_cmds} app commands for guild `{guild.name}` `({guild.id})`.",
        )

    @admin.subcommand(name="sync")
    async def sync(self, intr: Interaction[Any]) -> None:
        """(dev only) Synchronizes all app commands with Discord."""
        await intr.response.defer()
        await self._bot.client.sync_all_application_commands()
        await self._respond_successful(intr, "Synchronized app commands.")

    @admin.subcommand(name="shutdown", description="Shuts down the bot.")
    async def shutdown(self, intr: Interaction[Any]) -> None:
        """(dev only) Shutdowns the bot enitirely."""
        await self._respond_successful(intr, "Shutting down...")
        self._bot.app.stop()

    @admin.subcommand(name="whisper")
    async def whisper(self, intr: Interaction[Any], user_id: str, message: str) -> None:
        """(dev only) Whispers a message to a user.

        Parameters
        ----------
        user_id : str
            The user ID to whisper.
        message : str
            The message to whisper to the user.
        """
        user = await self._utils.must_get_user(user_id)

        try:
            await user.send(message)
        except nextcord.DiscordException as exc:
            raise ApplicationException(
                f"Failed whispering message to user {user.display_name}: `{exc}`"
            ) from exc

        await self._respond_successful(
            intr, f"Whispered message to `{user.name} ({user.id})`"
        )

    @admin.subcommand(name="whitelist")
    async def whitelist(
        self, intr: Interaction[Any], guild_id: str, until: str | None = None
    ) -> None:
        """(dev only) Whitelists or unwhitelists a guild from using the bot.

        Parameters
        ----------
        guild_id : str
            The guild ID to whitelist.
        until : str | None, optional
            Date until the whitelist expires, by default None
        """
        guild = await self._utils.must_get_guild(guild_id)

        async with self._enter_botdb_session() as (db, s):
            repo = db.whitelist_group

            if await repo.is_whitelisted_guild(guild.id, session=s):
                raise InvalidActionException(
                    f"Guild `{guild.name}` ({guild.id})` is already whitelisted"
                )

            await repo.whitelist_guild(
                guild.id,
                until=Utils.must_parse_date_string(until) if until else None,
                session=s,
            )

        await self._respond_successful(
            intr, f"Whitelisted guild `{guild.name} ({guild.id})`"
        )

    @admin.subcommand(name="unwhitelist")
    async def unwhitelist(self, intr: Interaction[Any], guild_id: str) -> None:
        """(dev only) Unwhitelists a guild from using the bot.

        Parameters
        ----------
        guild_id : str
            The guild ID to unwhitelist.
        """
        guild = await self._utils.must_get_guild(guild_id)

        async with self._enter_botdb_session() as (db, s):
            repo = db.whitelist_group

            if not await repo.is_whitelisted_guild(guild.id, session=s):
                raise InvalidActionException(
                    f"Guild `{guild.name} ({guild.id})` is not whitelisted"
                )

            await repo.unwhitelist_guild(guild.id, session=s)

        await self._respond_successful(
            intr, f"Unwhitelisted guild `{guild.name} ({guild.id})`"
        )

    @admin.subcommand(name="execute")
    async def execute(self, intr: Interaction[Any], command: str) -> None:
        """(dev only) Execute `command` directly to the host device.

        Parameters
        ----------
        command : str
            The command to execute.
        """
        command_ = command.split(" ")
        result = subprocess.run(command_, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            success_msg = (
                f"Command executed successfully!\nOutput:\n```\n{result.stdout}```"
            )
            await self._respond_successful(intr, success_msg)
        else:
            err_msg = f"Error executing command.\nError message:\n```\n{result.stderr}"
            raise ApplicationException(err_msg)

    def _is_channel_sendable(self, channel: object) -> bool:
        return hasattr(channel, "send")
