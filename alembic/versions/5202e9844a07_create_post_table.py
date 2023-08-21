"""create post table

Revision ID: 5202e9844a07
Revises: f61b492e5e83
Create Date: 2023-08-20 16:41:58.234925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5202e9844a07'
down_revision: Union[str, None] = 'f61b492e5e83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('body', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.text("now()"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('posts')
