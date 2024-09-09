## [0.1.3](https://github.com/FAZuH/faz-bot/compare/v0.1.2...v0.1.3) (2024-09-09)


### Bug Fixes

* fix undefined variable [skip ci] ([#29](https://github.com/FAZuH/faz-bot/issues/29)) ([78b7e0b](https://github.com/FAZuH/faz-bot/commit/78b7e0bcacb3b950a47a8643f48cfde7b09ea37c))


### Performance Improvements

* improve api performance ([#30](https://github.com/FAZuH/faz-bot/issues/30)) ([45252a1](https://github.com/FAZuH/faz-bot/commit/45252a1e259a5914e1bd84dc0ae1500b72c37c24))



## [0.1.2](https://github.com/FAZuH/faz-bot/compare/v0.1.1...v0.1.2) (2024-09-08)



## [0.1.1](https://github.com/FAZuH/faz-bot/compare/v0.1.0...v0.1.1) (2024-09-08)



# [0.1.0](https://github.com/FAZuH/faz-bot/compare/d4db3299f8c2d4fda51bd5e988f7e609807b0467...v0.1.0) (2024-09-08)


### Bug Fixes

* **api:** Fix WynnApi occasionally throwing KeyError ([#14](https://github.com/FAZuH/faz-bot/issues/14)) ([6789d21](https://github.com/FAZuH/faz-bot/commit/6789d21bff669027b60d7f878e1bc01fb876ce17))
* faz-db and faz-bot starts before mysql is ready to accept connections ([d4db329](https://github.com/FAZuH/faz-bot/commit/d4db3299f8c2d4fda51bd5e988f7e609807b0467))
* **fazdb:** Fix missing asyncio import on Main ([5413018](https://github.com/FAZuH/faz-bot/commit/5413018b2790a7068c51949e402c323565a642ae))
* **fazdb:** Fix TaskApiRequest stopping on api error ([3491a20](https://github.com/FAZuH/faz-bot/commit/3491a20a8a14e138a53f5f13aa859ad84d96b762))
* **fazdb:** TaskDbInsert not replacing info tables with new data ([7732a1e](https://github.com/FAZuH/faz-bot/commit/7732a1e1b370cdff6c4502f5a3a2da22037798ee))
* **fazutil.api:** fix some fields in Player model containing None ([874f427](https://github.com/FAZuH/faz-bot/commit/874f42701b3ff032c5bfd370138df7af018ccd1c))
* **fazutil.db:** fix typo on DiscordGuild variable name ([5224879](https://github.com/FAZuH/faz-bot/commit/522487906c217dd767c7a63c413ca4374ba43a67))
* fix guild_activity command not showing buttons ([2e34239](https://github.com/FAZuH/faz-bot/commit/2e34239a2f20b0315310cb6e6c0c0fead165faf1))
* fix inactive players shown on guild_activity command ([6e1ca7e](https://github.com/FAZuH/faz-bot/commit/6e1ca7e384211b0f23608a237847fa3a28cbb730))
* Fix incorrect log directory ([6ea1ae7](https://github.com/FAZuH/faz-bot/commit/6ea1ae76677cb35fde3f5020182430770440cf0e))
* Fix incorrect LOG_DIR path ([827a4bd](https://github.com/FAZuH/faz-bot/commit/827a4bd9e194d6bc31459c83605075d275686332))
* **github-actions:** fix release workflow failing to trigger ([b08f575](https://github.com/FAZuH/faz-bot/commit/b08f575c50b15b04d9738015b4eb6f34c6d0603d))
* incorrect log file paths ([819f8ac](https://github.com/FAZuH/faz-bot/commit/819f8ac066bca80216f42863ad60ca5d6b394b32))
* **logging:** error not properly handled by loguru ([2eda042](https://github.com/FAZuH/faz-bot/commit/2eda0421bf9e74798f5a3875087de8c49a60c6d6))
* TaskDbInsert receiving constraint error when inserting PlayerInfo ([30f46da](https://github.com/FAZuH/faz-bot/commit/30f46da30733ff06786cb7a1fbdd6c11a10f8f12))


### Features

* Add prometheus and grafana service ([cde103b](https://github.com/FAZuH/faz-bot/commit/cde103bd2ed8d3afc8787b45d3bad622383358a0))
* **bot:** add WynnTrackCog [skip ci] ([#20](https://github.com/FAZuH/faz-bot/issues/20)) ([114e2d0](https://github.com/FAZuH/faz-bot/commit/114e2d0716ad9d18ba5a016ed7fbd59742e6c4cb))
* **fazbot.bot:** add guild_activity command ([1fe3c1d](https://github.com/FAZuH/faz-bot/commit/1fe3c1de1e42978af70c15e47d25df163ccbba3b))
* **fazbot:** add activity command ([661ddea](https://github.com/FAZuH/faz-bot/commit/661ddea5a8fadfefdec4b611a6b8b4ea6a0617e3))
* **fazutil.db.fazdb:** add get_guild method to GuildInfo ([573425d](https://github.com/FAZuH/faz-bot/commit/573425d6469ae4f199a6bbbb351c6b1d910790e9))
* **fazutil.db:** Add DiscordGuild and DiscordUser table ([c91efd7](https://github.com/FAZuH/faz-bot/commit/c91efd7e116fe146181401b717b8d11aedaac239))
* Merged repositories `faz-bot` and `faz-db` into `faz-docker` ([bb58d75](https://github.com/FAZuH/faz-bot/commit/bb58d753c47b04abea5a9c5efa8fc2187e9c8632))


### Performance Improvements

* **fazutil.db:** add indexes on frequently used columns ([9b013e1](https://github.com/FAZuH/faz-bot/commit/9b013e1bf588ea83ae5eb626d894a0f49458eefa))


### Reverts

* Revert "chore: switch linter from flake8 to pylint" ([3f749c1](https://github.com/FAZuH/faz-bot/commit/3f749c1be81806bb4603c1f0c865a7706f9de73e))



