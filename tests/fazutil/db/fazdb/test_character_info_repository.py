from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, override

from fazutil.db.fazdb.repository.character_info_repository import (
    CharacterInfoRepository,
)
from tests.fazutil.db.fazdb._common_fazdb_repository_test import (
    CommonFazdbRepositoryTest,
)

if TYPE_CHECKING:
    from fazutil.db.fazdb.model.character_history import CharacterHistory


class TestCharacterInfoRepository(
    CommonFazdbRepositoryTest.Test[CharacterInfoRepository]
):
    async def __prepare_char_history(self) -> tuple[CharacterHistory, CharacterHistory]:
        mock_info = self._get_mock_data()[0]
        mocks_history = self._get_character_history_mock_data()

        mocksh1, mocksh2 = mocks_history[0], mocks_history[1]
        mocksh2.level += 1
        mocksh2.datetime = mocksh2.datetime + timedelta(seconds=10)
        mocksh2._compute_unique_id()

        await self.repo.insert(mock_info)
        await self.database.character_history.insert([mocksh1, mocksh2])
        return mocksh1, mocksh2

    async def test_latest_stat_relationship(self) -> None:
        # Prepare
        mocksh = (await self.__prepare_char_history())[1]

        # Act
        async with self.database.enter_async_session() as ses:
            res_info = await self.repo.select_all(session=ses)
            info = res_info[0]
            await info.awaitable_attrs.latest_stat
            self.assertEqual(info.latest_stat, mocksh)

    async def test_stat_history_relationship(self) -> None:
        # Prepare
        mocksh1, mocksh2 = await self.__prepare_char_history()

        # Act
        async with self.database.enter_async_session() as ses:
            res_info = await self.repo.select_all(session=ses)
            info = res_info[0]
            await info.awaitable_attrs.stat_history
            self.assertCountEqual(info.stat_history, [mocksh1, mocksh2])

    async def test_select_from_player(self) -> None:
        # Prepare
        mock_ch = self._get_mock_data()
        mock_ch[2].uuid = mock_ch[0].uuid
        await self.repo.insert([mock_ch[0], mock_ch[2]])

        # Act
        res = await self.repo.select_from_player(mock_ch[0].uuid)

        # Assert
        self.assertCountEqual(res, [mock_ch[0], mock_ch[2]])

    @override
    async def _create_table(self) -> None:
        self.database.create_all()
        mock_player = self._get_player_info_mock_data()
        await self.database.player_info.insert([mock_player[0], mock_player[2]])

    @override
    def _get_mock_data(self):
        return self._get_character_info_mock_data()

    @property
    @override
    def repo(self):
        return self.database.character_info
