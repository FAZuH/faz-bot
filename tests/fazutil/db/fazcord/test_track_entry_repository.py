from typing import override

from fazutil.db.fazcord.repository.track_entry_repository import TrackEntryRepository
from tests.fazutil.db.fazcord._common_fazcord_repository_test import (
    CommonFazcordRepositoryTest,
)


class TestTrackEntryRepository(CommonFazcordRepositoryTest.Test[TrackEntryRepository]):
    async def test_insert_get_id_after(self) -> None:
        # TODO: just testing if this works
        # Prepare
        mock_data1 = self.repo.model(channel_id=1, created_by=1, type="GUILD")
        mock_data2 = self.repo.model(channel_id=2, created_by=1, type="GUILD")
        # Act, Assert
        self.assertEqual(mock_data1.id, None)
        self.assertEqual(mock_data2.id, None)
        await self.repo.insert(mock_data1)
        self.assertEqual(mock_data1.id, 1)
        self.assertEqual(mock_data2.id, None)
        await self.repo.insert(mock_data2)
        self.assertEqual(mock_data1.id, 1)
        self.assertEqual(mock_data2.id, 2)

    async def test_toggle_on(self) -> None:
        # Prepare
        mock_data = self._get_mock_data()[0]
        mock_data.enabled = True
        await self.repo.insert(mock_data)
        # Act
        ret = await self.repo.toggle(1)
        # Assert
        res = await self.repo.select_all()
        self.assertEqual(res[0].enabled, False)
        self.assertEqual(ret, False)

    async def test_toggle_off(self) -> None:
        # Prepare
        mock_data = self._get_mock_data()[0]
        mock_data.enabled = False
        await self.repo.insert(mock_data)
        # Act
        ret = await self.repo.toggle(1)
        # Assert
        res = await self.repo.select_all()
        self.assertEqual(res[0].enabled, True)
        self.assertEqual(ret, True)

    async def test_select_by_channel_id_exist(self) -> None:
        # Prepare
        mock_data = self._get_mock_data()[0]
        await self.repo.insert(mock_data)
        # Act
        res = await self.repo.select_by_channel_id(1)
        # Assert
        self.assertEqual(res, mock_data)

    async def test_select_by_channel_id_not_exist(self) -> None:
        # Act
        res = await self.repo.select_by_channel_id(999)
        # Assert
        self.assertIsNone(res)

    async def test_select_by_guild_id(self) -> None:
        # Prepare
        mock_data = self._get_mock_data()
        to_insert = [mock_data[0], mock_data[2]]
        await self.repo.insert(to_insert)
        # Act
        res = await self.repo.select_by_guild_id(1)
        # Assert
        self.assertEqual(len(res), 2)
        self.assertEqual(res, to_insert)

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
        async with db.enter_async_session() as ses:
            await db.discord_guild_repository.insert([mock_guild[0]], session=ses)
            await db.discord_channel_repository.insert(
                [mock_channel[0], mock_channel[2]], session=ses
            )
            await db.discord_user_repository.insert([mock_user[0]], session=ses)

    @override
    def _get_mock_data(self):
        return self._get_track_entry_mock_data()

    @property
    @override
    def repo(self):
        return self.database.track_entry_repository
