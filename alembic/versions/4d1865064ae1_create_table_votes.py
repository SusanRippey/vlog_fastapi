"""create table votes

Revision ID: 4d1865064ae1
Revises: 576f8a9165ac
Create Date: 2023-08-21 08:39:45.008642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d1865064ae1'
down_revision: Union[str, None] = '576f8a9165ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'votes',
        sa.Column('user_id', sa.INTEGER(), nullable=False),
        sa.Column('post_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(columns=['post_id'],refcolumns=['posts.id'],ondelete="CASCADE"),
        sa.ForeignKeyConstraint(columns=['user_id'],refcolumns=['users.id'],ondelete="CASCADE"),
        sa.PrimaryKeyConstraint('user_id','post_id')
    )


def downgrade() -> None:
    op.drop_table('votes')
