"""Initial migration

Revision ID: bba3742a6166
Revises: d7fcd314280b
Create Date: 2024-09-18 09:39:05.085034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'bba3742a6166'
down_revision: Union[str, None] = 'd7fcd314280b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pro_series', sa.Column('series_type', mysql.TINYINT(), nullable=True, comment='1-Parent, 2-child'))
    op.drop_column('pro_series', 'seies_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pro_series', sa.Column('seies_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-Parent, 2-child'))
    op.drop_column('pro_series', 'series_type')
    # ### end Alembic commands ###
