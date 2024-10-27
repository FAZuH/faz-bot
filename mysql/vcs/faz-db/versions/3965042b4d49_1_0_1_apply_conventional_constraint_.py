"""1.0.1 Apply conventional constraint naming

Revision ID: 3965042b4d49
Revises: 339ac85161c0
Create Date: 2024-10-27 17:18:29.407329

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3965042b4d49"
down_revision: Union[str, None] = "339ac85161c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# fmt: off
def upgrade():
    # Drop old indexes
    op.drop_index("logon_datetime_idx", table_name="player_activity_history")
    op.drop_index("logoff_datetime_idx", table_name="player_activity_history")
    op.drop_index("unique_id_idx", table_name="guild_history")
    op.drop_index("datetime_idx", table_name="guild_history")
    op.drop_index("unique_id_idx", table_name="guild_member_history")
    op.drop_index("datetime_idx", table_name="guild_member_history")
    op.drop_index("unique_id_idx", table_name="player_history")
    op.drop_index("datetime_idx", table_name="player_history")
    op.drop_index("unique_id_idx", table_name="character_history")
    op.drop_index("datetime_idx", table_name="character_history")

    # Create new indexes with conventional names
    op.create_unique_constraint(None, "guild_history", ["unique_id"])
    op.create_unique_constraint(None, "guild_member_history", ["unique_id"])
    op.create_unique_constraint(None, "player_history", ["unique_id"])
    op.create_unique_constraint(None, "character_history", ["unique_id"])
    op.create_index(None, "player_activity_history", ["logon_datetime"])
    op.create_index(None, "player_activity_history", ["logoff_datetime"])
    op.create_index(None, "guild_history", ["datetime"])
    op.create_index(None, "guild_member_history", ["datetime"])
    op.create_index(None, "player_history", ["datetime"])
    op.create_index(None, "character_history", ["datetime"])


def downgrade():
    # Drop the new constraints and indexes
    op.drop_constraint("uq_character_history_unique_id", "character_history", type_="unique")
    op.drop_constraint("uq_player_history_unique_id", "player_history", type_="unique")
    op.drop_constraint("uq_guild_member_history_unique_id", "guild_member_history", type_="unique")
    op.drop_constraint("uq_guild_history_unique_id", "guild_history", type_="unique")
    op.drop_index("ix_character_history_datetime", table_name="character_history")
    op.drop_index("ix_player_history_datetime", table_name="player_history")
    op.drop_index("ix_guild_member_history_datetime", table_name="guild_member_history")
    op.drop_index("ix_guild_history_datetime", table_name="guild_history")
    op.drop_index("ix_player_activity_history_logon_datetime", table_name="player_activity_history")
    op.drop_index("ix_player_activity_history_logoff_datetime", table_name="player_activity_history")

    # Recreate old indexes
    op.create_index("logon_datetime_idx", "player_activity_history", ["logon_datetime"], unique=False,)
    op.create_index("logoff_datetime_idx", "player_activity_history", ["logoff_datetime"], unique=False,)
    op.create_index("unique_id_idx", "guild_history", ["unique_id"], unique=True)
    op.create_index("datetime_idx", "guild_history", ["datetime"], unique=False)
    op.create_index("unique_id_idx", "guild_member_history", ["unique_id"], unique=True)
    op.create_index("datetime_idx", "guild_member_history", ["datetime"], unique=False)
    op.create_index("unique_id_idx", "player_history", ["unique_id"], unique=True)
    op.create_index("datetime_idx", "player_history", ["datetime"], unique=False)
    op.create_index("unique_id_idx", "character_history", ["unique_id"], unique=True)
    op.create_index("datetime_idx", "character_history", ["datetime"], unique=False)
# fmt: on
