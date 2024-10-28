"""1.0.0 Initial faz-db version

Revision ID: 339ac85161c0
Revises: 
Create Date: 2024-10-26 13:30:38.564124

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "339ac85161c0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "character_history",
        sa.Column("character_uuid", sa.BINARY(length=16), nullable=False),
        sa.Column(
            "level", mysql.TINYINT(display_width=4), autoincrement=False, nullable=False
        ),
        sa.Column(
            "xp", mysql.BIGINT(display_width=20), autoincrement=False, nullable=False
        ),
        sa.Column(
            "wars", mysql.INTEGER(display_width=11), autoincrement=False, nullable=False
        ),
        sa.Column("playtime", mysql.DECIMAL(precision=7, scale=2), nullable=False),
        sa.Column(
            "mobs_killed",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "chests_found",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "logins",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "deaths",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "discoveries",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "hardcore",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "ultimate_ironman",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "ironman",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "craftsman",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "hunted",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("alchemism", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("armouring", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("cooking", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("jeweling", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("scribing", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("tailoring", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column(
            "weaponsmithing", mysql.DECIMAL(precision=5, scale=2), nullable=False
        ),
        sa.Column("woodworking", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("mining", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("woodcutting", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("farming", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column("fishing", mysql.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column(
            "dungeon_completions",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "quest_completions",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "raid_completions",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("datetime", mysql.DATETIME(), nullable=False),
        sa.Column("unique_id", sa.BINARY(length=16), nullable=False),
        sa.PrimaryKeyConstraint("character_uuid", "datetime"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "character_info",
        sa.Column("character_uuid", sa.BINARY(length=16), nullable=False),
        sa.Column("uuid", sa.BINARY(length=16), nullable=False),
        sa.Column(
            "type",
            mysql.ENUM("ARCHER", "ASSASSIN", "MAGE", "SHAMAN", "WARRIOR"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("character_uuid"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "fazdb_uptime",
        sa.Column("start_time", mysql.DATETIME(), nullable=False),
        sa.Column("stop_time", mysql.DATETIME(), nullable=False),
        sa.PrimaryKeyConstraint("start_time"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "guild_history",
        sa.Column("name", mysql.VARCHAR(length=30), nullable=False),
        sa.Column(
            "level", mysql.DECIMAL(unsigned=True, precision=5, scale=2), nullable=False
        ),
        sa.Column(
            "territories",
            mysql.SMALLINT(display_width=5, unsigned=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "wars",
            mysql.INTEGER(display_width=10, unsigned=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "member_total",
            mysql.TINYINT(display_width=3, unsigned=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "online_members",
            mysql.TINYINT(display_width=3, unsigned=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("datetime", mysql.DATETIME(), nullable=False),
        sa.Column("unique_id", sa.BINARY(length=16), nullable=False),
        sa.PrimaryKeyConstraint("name", "datetime"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "guild_info",
        sa.Column("uuid", sa.BINARY(length=16), nullable=False),
        sa.Column("name", mysql.VARCHAR(length=30), nullable=False),
        sa.Column("prefix", mysql.VARCHAR(length=4), nullable=False),
        sa.Column("created", mysql.DATETIME(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "guild_member_history",
        sa.Column("uuid", sa.BINARY(length=16), nullable=False),
        sa.Column(
            "contributed",
            mysql.BIGINT(display_width=20, unsigned=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("joined", mysql.DATETIME(), nullable=False),
        sa.Column("datetime", mysql.DATETIME(), nullable=False),
        sa.Column("unique_id", sa.BINARY(length=16), nullable=False),
        sa.PrimaryKeyConstraint("uuid", "joined"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "online_players",
        sa.Column("uuid", sa.BINARY(length=16), nullable=False),
        sa.Column("server", mysql.VARCHAR(length=10), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "player_activity_history",
        sa.Column("uuid", sa.BINARY(length=16), nullable=False),
        sa.Column("logon_datetime", mysql.DATETIME(), nullable=False),
        sa.Column("logoff_datetime", mysql.DATETIME(), nullable=False),
        sa.PrimaryKeyConstraint("uuid", "logon_datetime"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "player_history",
        sa.Column("uuid", sa.BINARY(length=16), nullable=False),
        sa.Column("username", mysql.VARCHAR(length=16), nullable=False),
        sa.Column("support_rank", mysql.VARCHAR(length=45), nullable=False),
        sa.Column(
            "playtime",
            mysql.DECIMAL(unsigned=True, precision=8, scale=2),
            nullable=False,
        ),
        sa.Column("guild_name", mysql.VARCHAR(length=30), nullable=False),
        sa.Column(
            "guild_rank",
            mysql.ENUM(
                "OWNER", "CHIEF", "STRATEGIST", "CAPTAIN", "RECRUITER", "RECRUIT"
            ),
            nullable=False,
        ),
        sa.Column("rank", mysql.VARCHAR(length=30), nullable=False),
        sa.Column("datetime", mysql.DATETIME(), nullable=False),
        sa.Column("unique_id", sa.BINARY(length=16), nullable=False),
        sa.PrimaryKeyConstraint("uuid", "datetime"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "worlds",
        sa.Column("name", mysql.VARCHAR(length=16), nullable=False),
        sa.Column(
            "player_count",
            mysql.SMALLINT(display_width=5, unsigned=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("time_created", mysql.DATETIME(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "player_info",
        sa.Column("uuid", sa.BINARY(length=16), nullable=False),
        sa.Column("latest_username", mysql.VARCHAR(length=16), nullable=False),
        sa.Column("first_join", mysql.DATETIME(), nullable=False),
        sa.Column("guild_uuid", sa.BINARY(length=16), nullable=True),
        sa.ForeignKeyConstraint(
            ["guild_uuid"], ["guild_info.uuid"], name="fk_guild_uuid"
        ),
        sa.PrimaryKeyConstraint("uuid"),
        mysql_collate="utf8mb4_uca1400_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )

    op.create_index(
        "logon_datetime_idx",
        "player_activity_history",
        ["logon_datetime"],
        unique=False,
    )
    op.create_index(
        "logoff_datetime_idx",
        "player_activity_history",
        ["logoff_datetime"],
        unique=False,
    )
    op.create_index("unique_id_idx", "guild_history", ["unique_id"], unique=True)
    op.create_index("datetime_idx", "guild_history", ["datetime"], unique=False)
    op.create_index("unique_id_idx", "guild_member_history", ["unique_id"], unique=True)
    op.create_index("datetime_idx", "guild_member_history", ["datetime"], unique=False)
    op.create_index("unique_id_idx", "player_history", ["unique_id"], unique=True)
    op.create_index("datetime_idx", "player_history", ["datetime"], unique=False)
    op.create_index("unique_id_idx", "character_history", ["unique_id"], unique=True)
    op.create_index("datetime_idx", "character_history", ["datetime"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # raise ValueError(
    #     "Downgrade is not supported here. run `python -m alembic stamp base` to checkout to base."
    # )
    op.drop_table("character_history")
    op.drop_table("guild_history")
    op.drop_table("player_history")

    op.drop_table("character_info")
    op.drop_table("player_info")
    op.drop_table("guild_info")

    op.drop_table("guild_member_history")
    op.drop_table("player_activity_history")
    op.drop_table("online_players")
    op.drop_table("fazdb_uptime")
    op.drop_table("worlds")
