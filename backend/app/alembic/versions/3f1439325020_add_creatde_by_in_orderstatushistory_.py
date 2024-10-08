"""add creatde by in OrderStatusHistory table

Revision ID: 3f1439325020
Revises: e04a9bb3a034
Create Date: 2024-08-23 17:07:16.796828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f1439325020'
down_revision: Union[str, None] = 'e04a9bb3a034'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('title', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'title')
    # ### end Alembic commands ###
