"""add creatde by in OrderStatusHistory table

Revision ID: f8a0899448c8
Revises: 89d21ca45122
Create Date: 2024-08-28 10:01:27.648581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f8a0899448c8'
down_revision: Union[str, None] = '89d21ca45122'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('careers', 'employement_type',
               existing_type=mysql.TINYINT(),
               comment='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary,6-hyper',
               existing_comment='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('careers', 'employement_type',
               existing_type=mysql.TINYINT(),
               comment='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary',
               existing_comment='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary,6-hyper',
               existing_nullable=True)
    # ### end Alembic commands ###
