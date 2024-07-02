### ----- faz-db database create tables -----

USE `faz-db`;

CREATE TABLE IF NOT EXISTS `character_history` (
    `character_uuid` binary(16) NOT NULL,
    `level` tinyint unsigned NOT NULL,
    `xp` bigint unsigned NOT NULL,
    `wars` int unsigned NOT NULL,
    `playtime` decimal(7,2) unsigned NOT NULL,
    `mobs_killed` int unsigned NOT NULL,
    `chests_found` int unsigned NOT NULL,
    `logins` int unsigned NOT NULL,
    `deaths` int unsigned NOT NULL,
    `discoveries` int unsigned NOT NULL,
    `hardcore` boolean NOT NULL,
    `ultimate_ironman` boolean NOT NULL,
    `ironman` boolean NOT NULL,
    `craftsman` boolean NOT NULL,
    `hunted` boolean NOT NULL,
    `alchemism` decimal(5,2) unsigned NOT NULL,
    `armouring` decimal(5,2) unsigned NOT NULL,
    `cooking` decimal(5,2) unsigned NOT NULL,
    `jeweling` decimal(5,2) unsigned NOT NULL,
    `scribing` decimal(5,2) unsigned NOT NULL,
    `tailoring` decimal(5,2) unsigned NOT NULL,
    `weaponsmithing` decimal(5,2) unsigned NOT NULL,
    `woodworking` decimal(5,2) unsigned NOT NULL,
    `mining` decimal(5,2) unsigned NOT NULL,
    `woodcutting` decimal(5,2) unsigned NOT NULL,
    `farming` decimal(5,2) unsigned NOT NULL,
    `fishing` decimal(5,2) unsigned NOT NULL,
    `dungeon_completions` int unsigned NOT NULL,
    `quest_completions` int unsigned NOT NULL,
    `raid_completions` int unsigned NOT NULL,
    `datetime` datetime NOT NULL,
    `unique_id` binary(16) NOT NULL,
    PRIMARY KEY (`character_uuid`,`datetime`),
    UNIQUE KEY `unique_id_idx` (`unique_id`),
    KEY `datetime_idx` (`datetime` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `character_info` (
    `character_uuid` binary(16) NOT NULL,
    `uuid` binary(16) NOT NULL,
    `type` enum('ARCHER','ASSASSIN','MAGE','SHAMAN','WARRIOR') NOT NULL,
    PRIMARY KEY (`character_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `fazdb_uptime` (
    `start_time` datetime PRIMARY KEY NOT NULL,
    `stop_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `guild_history` (
    `name` varchar(30) NOT NULL,
    `level` decimal(5,2) unsigned NOT NULL,
    `territories` smallint unsigned NOT NULL,
    `wars` int unsigned NOT NULL,
    `member_total` tinyint unsigned NOT NULL,
    `online_members` tinyint unsigned NOT NULL,
    `datetime` datetime NOT NULL,
    `unique_id` binary(16) NOT NULL,
    PRIMARY KEY (`name`,`datetime`),
    UNIQUE KEY `unique_id_idx` (`unique_id`),
    KEY `datetime_idx` (`datetime` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `guild_info` (
    `name` varchar(30) PRIMARY KEY NOT NULL,
    `prefix` varchar(4) NOT NULL,
    `created` datetime NOT NULL,
    `uuid` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `guild_member_history` (
    `uuid` binary(16) NOT NULL,
    `contributed` bigint unsigned NOT NULL,
    `joined` datetime NOT NULL,
    `datetime` datetime NOT NULL,
    `unique_id` binary(16) NOT NULL,
    PRIMARY KEY (`uuid`,`datetime`),
    UNIQUE KEY `unique_id_idx` (`unique_id`),
    KEY `datetime_idx` (`datetime` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `online_players` (
    `uuid` binary(16) PRIMARY KEY NOT NULL,
    `server` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `player_activity_history` (
    `uuid` binary(16) NOT NULL,
    `logon_datetime` datetime NOT NULL,
    `logoff_datetime` datetime NOT NULL,
    PRIMARY KEY (`uuid`,`logon_datetime`),
    KEY `logon_datetime` (`logon_datetime` DESC),
    KEY `logoff_datetime` (`logoff_datetime` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `player_history` (
    `uuid` binary(16) NOT NULL,
    `username` varchar(16) NOT NULL,
    `support_rank` varchar(45) DEFAULT NULL,
    `playtime` decimal(8,2) unsigned NOT NULL,
    `guild_name` varchar(30) DEFAULT NULL,
    `guild_rank` enum('OWNER','CHIEF','STRATEGIST','CAPTAIN','RECRUITER','RECRUIT') DEFAULT NULL,
    `rank` varchar(30) DEFAULT NULL,
    `datetime` datetime NOT NULL,
    `unique_id` binary(16) NOT NULL,
    PRIMARY KEY (`uuid`,`datetime`),
    UNIQUE KEY `unique_id_idx` (`unique_id`),
    KEY `datetime_idx` (`datetime` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `player_info` (
    `uuid` binary(16) NOT NULL,
    `latest_username` varchar(16) NOT NULL,
    `first_join` datetime NOT NULL,
    PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
