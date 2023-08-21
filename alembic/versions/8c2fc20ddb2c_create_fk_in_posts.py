"""create fk in posts

Revision ID: 8c2fc20ddb2c
Revises: 5202e9844a07
Create Date: 2023-08-20 16:56:13.544076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c2fc20ddb2c'
down_revision: Union[str, None] = '5202e9844a07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key(constraint_name="posts_fk_user", source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'])

def downgrade() -> None:
    op.drop_constraint('posts_fk_user', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
