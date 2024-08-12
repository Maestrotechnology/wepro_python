"""add file type in article files

Revision ID: d4bd3fa06aea
Revises: ac45c587ee4d
Create Date: 2024-08-05 10:15:30.391206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4bd3fa06aea'
down_revision: Union[str, None] = 'ac45c587ee4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('content_created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'content_created_at')
    # ### end Alembic commands ###