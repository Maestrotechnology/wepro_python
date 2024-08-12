"""add file type in article files

Revision ID: 47c49fd8430c
Revises: 4def81aa85a2
Create Date: 2024-08-05 10:04:10.342172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47c49fd8430c'
down_revision: Union[str, None] = '4def81aa85a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('topic_review_at', sa.DateTime(), nullable=True))
    op.add_column('article', sa.Column('topic_cmnt_at', sa.DateTime(), nullable=True))
    op.add_column('article', sa.Column('content_review_at', sa.DateTime(), nullable=True))
    op.add_column('article', sa.Column('content_cmnt_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'content_cmnt_at')
    op.drop_column('article', 'content_review_at')
    op.drop_column('article', 'topic_cmnt_at')
    op.drop_column('article', 'topic_review_at')
    # ### end Alembic commands ###