"""add ad table

Revision ID: c3e1e5c76551
Revises: 439e31c9d180
Create Date: 2024-07-17 16:48:14.317529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c3e1e5c76551'
down_revision: Union[str, None] = '439e31c9d180'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_ibfk_2', 'user', type_='foreignkey')
    op.drop_constraint('user_ibfk_4', 'user', type_='foreignkey')
    op.drop_column('user', 'state_id')
    op.drop_column('user', 'city_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('city_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('state_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_ibfk_4', 'user', 'states', ['state_id'], ['id'])
    op.create_foreign_key('user_ibfk_2', 'user', 'cities', ['city_id'], ['id'])
    # ### end Alembic commands ###
