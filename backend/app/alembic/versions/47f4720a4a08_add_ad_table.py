"""add ad table

Revision ID: 47f4720a4a08
Revises: 3dd1170ed284
Create Date: 2024-07-16 15:06:16.208710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '47f4720a4a08'
down_revision: Union[str, None] = '3dd1170ed284'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('advertisement', 'ad_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisement', sa.Column('ad_url', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
