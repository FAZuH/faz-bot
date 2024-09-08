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

    async def test_cascade_on_track_entry_delete(self) -> None:
        # Prepare
        mock_data = self._get_mock_data()[0]
        await self.repo.insert(mock_data)
        print(await self.repo.select_all())
        print(await self.database.track_entry_repository.select_all())
        # Act
        await self.database.track_entry_repository.delete(1)
        # Assert
        res = await self.repo.select_all()
        self.assertEqual(len(res), 0)

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
        async with db.enter_async_session() as ses:
            await db.discord_guild_repository.insert([mock_guild[0]], session=ses)
            await db.discord_channel_repository.insert(
                [mock_channel[0], mock_channel[2]], session=ses
            )
            await db.discord_user_repository.insert([mock_user[0]], session=ses)
            await db.track_entry_repository.insert(
                [mock_track[0], mock_track[2]], session=ses
            )

    @override
    def _get_mock_data(self):
        return self._get_track_entry_association_mock_data()

    @property
    @override
    def repo(self):
        return self.database.track_entry_association_repository
