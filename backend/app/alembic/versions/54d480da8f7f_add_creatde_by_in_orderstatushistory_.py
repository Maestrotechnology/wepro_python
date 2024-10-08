"""add creatde by in OrderStatusHistory table

Revision ID: 54d480da8f7f
Revises: f703c928cabf
Create Date: 2024-08-23 14:23:01.840645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54d480da8f7f'
down_revision: Union[str, None] = 'f703c928cabf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_history', sa.Column('topic_id', sa.Integer(), nullable=True, comment='topic tab id'))
    op.create_foreign_key(None, 'article_history', 'article_topic', ['topic_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'article_history', type_='foreignkey')
    op.drop_column('article_history', 'topic_id')
    # ### end Alembic commands ###
