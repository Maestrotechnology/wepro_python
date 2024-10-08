"""add creatde by in OrderStatusHistory table

Revision ID: 08ace977cb29
Revises: 847bf5ef8cec
Create Date: 2024-08-23 16:44:05.562246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08ace977cb29'
down_revision: Union[str, None] = '847bf5ef8cec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_history', sa.Column('article_state', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article_history', 'article_state')
    # ### end Alembic commands ###
