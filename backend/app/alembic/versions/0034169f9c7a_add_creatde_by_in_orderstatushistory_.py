"""add creatde by in OrderStatusHistory table

Revision ID: 0034169f9c7a
Revises: 9a209ca5ea40
Create Date: 2024-08-23 12:52:09.129272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '0034169f9c7a'
down_revision: Union[str, None] = '9a209ca5ea40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_history', 'history_type',
               existing_type=mysql.TINYINT(),
               comment='1->topic,2-content,3-editors_topic',
               existing_comment='1->topic,2-content',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_history', 'history_type',
               existing_type=mysql.TINYINT(),
               comment='1->topic,2-content',
               existing_comment='1->topic,2-content,3-editors_topic',
               existing_nullable=True)
    # ### end Alembic commands ###