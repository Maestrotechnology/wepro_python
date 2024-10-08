"""add topic and content status in article history

Revision ID: 052e63e0ed8d
Revises: b346c524246b
Create Date: 2024-07-30 09:08:47.662290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '052e63e0ed8d'
down_revision: Union[str, None] = 'b346c524246b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_history', sa.Column('topic_status', mysql.TINYINT(), nullable=True, comment='1->new,2-review,3-comment,4->SE approved,5-CE Approved'))
    op.add_column('article_history', sa.Column('content_status', mysql.TINYINT(), nullable=True, comment='1->new,2-review,3-comment,4->SE approved,5-Published(CE Approved)'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article_history', 'content_status')
    op.drop_column('article_history', 'topic_status')
    # ### end Alembic commands ###
