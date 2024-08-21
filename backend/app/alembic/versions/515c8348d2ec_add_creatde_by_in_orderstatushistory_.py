"""add creatde by in OrderStatusHistory table

Revision ID: 515c8348d2ec
Revises: 372a307d22a7
Create Date: 2024-08-21 14:42:08.393413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '515c8348d2ec'
down_revision: Union[str, None] = '372a307d22a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('save_for_later', mysql.TINYINT(), nullable=True, comment='1->yes'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'save_for_later')
    # ### end Alembic commands ###
