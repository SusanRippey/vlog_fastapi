"""alter column in post table

Revision ID: 576f8a9165ac
Revises: 8c2fc20ddb2c
Create Date: 2023-08-20 17:26:22.258211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '576f8a9165ac'
down_revision: Union[str, None] = '8c2fc20ddb2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('posts_fk_user', 'posts', type_='foreignkey')
    op.create_foreign_key(constraint_name="posts_fk_user", source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'])


def downgrade() -> None:
    pass
