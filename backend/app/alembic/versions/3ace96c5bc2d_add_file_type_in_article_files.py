"""add file type in article files

Revision ID: 3ace96c5bc2d
Revises: d4bd3fa06aea
Create Date: 2024-08-05 10:20:14.647082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ace96c5bc2d'
down_revision: Union[str, None] = 'd4bd3fa06aea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('topic_se_approved_at', sa.DateTime(), nullable=True))
    op.add_column('article', sa.Column('content_se_approved_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'content_se_approved_at')
    op.drop_column('article', 'topic_se_approved_at')
    # ### end Alembic commands ###
