"""add creatde by in OrderStatusHistory table

Revision ID: 68406a4b9b14
Revises: c4c02040bf67
Create Date: 2024-08-22 14:32:57.953045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '68406a4b9b14'
down_revision: Union[str, None] = 'c4c02040bf67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_history', sa.Column('is_editor', mysql.TINYINT(), nullable=True, comment='1->Se,-2->Ce'))
    op.alter_column('article_history', 'topic_status',
               existing_type=mysql.TINYINT(),
               comment='1->new,2-review,3-comment,4->approved',
               existing_comment='1->new,2-review,3-comment,4->SE approved,5-CE Approved',
               existing_nullable=True)
    op.alter_column('article_history', 'content_status',
               existing_type=mysql.TINYINT(),
               comment='1->new,2-review,3-comment,4->approved',
               existing_comment='1->new,2-review,3-comment,4->SE approved,5-Published(CE Approved),6-Deadline',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_history', 'content_status',
               existing_type=mysql.TINYINT(),
               comment='1->new,2-review,3-comment,4->SE approved,5-Published(CE Approved),6-Deadline',
               existing_comment='1->new,2-review,3-comment,4->approved',
               existing_nullable=True)
    op.alter_column('article_history', 'topic_status',
               existing_type=mysql.TINYINT(),
               comment='1->new,2-review,3-comment,4->SE approved,5-CE Approved',
               existing_comment='1->new,2-review,3-comment,4->approved',
               existing_nullable=True)
    op.drop_column('article_history', 'is_editor')
    # ### end Alembic commands ###
