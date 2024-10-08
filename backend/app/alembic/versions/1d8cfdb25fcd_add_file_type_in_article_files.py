"""add file type in article files

Revision ID: 1d8cfdb25fcd
Revises: 7ae4238fca06
Create Date: 2024-08-01 15:14:26.172959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1d8cfdb25fcd'
down_revision: Union[str, None] = '7ae4238fca06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('careers', sa.Column('experience_type', mysql.TINYINT(), nullable=True, comment='1-fresher, 2-experience'))
    op.add_column('careers', sa.Column('experience_year', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('careers', 'experience_year')
    op.drop_column('careers', 'experience_type')
    # ### end Alembic commands ###
