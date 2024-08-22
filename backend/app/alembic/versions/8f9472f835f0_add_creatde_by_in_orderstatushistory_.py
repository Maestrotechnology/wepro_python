"""add creatde by in OrderStatusHistory table

Revision ID: 8f9472f835f0
Revises: 4388558e57ec
Create Date: 2024-08-22 14:36:56.557886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8f9472f835f0'
down_revision: Union[str, None] = '4388558e57ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_history', sa.Column('history_type', mysql.TINYINT(), nullable=True, comment='1->topic,2-content'))
    op.drop_column('article_history', 'article_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_history', sa.Column('article_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->topic,2-content'))
    op.drop_column('article_history', 'history_type')
    # ### end Alembic commands ###
