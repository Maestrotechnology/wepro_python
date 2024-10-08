"""add creatde by in OrderStatusHistory table

Revision ID: db7d3ddf349a
Revises: 2bbf4d56a3b7
Create Date: 2024-08-29 09:23:54.291959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'db7d3ddf349a'
down_revision: Union[str, None] = '2bbf4d56a3b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_topic', sa.Column('comment', sa.String(length=250), nullable=True))
    op.alter_column('article_topic', 'is_approved',
               existing_type=mysql.TINYINT(),
               comment='1-approved,2-comment',
               existing_comment='1->comment,2-approved',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_topic', 'is_approved',
               existing_type=mysql.TINYINT(),
               comment='1->comment,2-approved',
               existing_comment='1-approved,2-comment',
               existing_nullable=True)
    op.drop_column('article_topic', 'comment')
    # ### end Alembic commands ###
