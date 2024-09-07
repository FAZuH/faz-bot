from typing import override

from fazutil.db.fazcord.repository.track_entry_association_repository import (
    TrackEntryAssociationRepository,
)
from tests.fazutil.db.fazcord._common_fazcord_repository_test import (
    CommonFazcordRepositoryTest,
)


class TestTrackEntryAssociationRepository(
    CommonFazcordRepositoryTest.Test[TrackEntryAssociationRepository]
):

    @override
    async def _create_table(self) -> None:
        db = self.database
        await db.discord_guild_repository.create_table()
        await db.discord_user_repository.create_table()
        await db.discord_channel_repository.create_table()
        await db.track_entry_repository.create_table()
        await db.track_entry_association_repository.create_table()
        mock_guild = self._get_discord_guild_mock_data()
        mock_channel = self._get_discord_channel_mock_data()
        mock_user = self._get_discord_user_mock_data()
        mock_track = self._get_track_entry_mock_data()
        await db.discord_guild_repository.insert([mock_guild[0]])
        await db.discord_channel_repository.insert([mock_channel[0]])
        await db.discord_user_repository.insert([mock_user[0]])
        await db.track_entry_repository.insert([mock_track[0]])

    @override
    def _get_mock_data(self):
        return self._get_track_entry_association_mock_data()

    @property
    @override
    def repo(self):
        return self.database.track_entry_association_repository
