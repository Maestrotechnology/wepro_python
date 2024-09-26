"""Initial migration

Revision ID: 8011910ede42
Revises: 3f4be8d97ada
Create Date: 2024-09-26 16:33:17.791767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8011910ede42'
down_revision: Union[str, None] = '3f4be8d97ada'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article_files', 'raw_file')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_files', sa.Column('raw_file', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
