"""add creatde by in OrderStatusHistory table

Revision ID: d85c04b1cf12
Revises: 7b4bebc8a737
Create Date: 2024-08-27 16:29:00.266538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd85c04b1cf12'
down_revision: Union[str, None] = '7b4bebc8a737'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media_files', sa.Column('start_date', sa.Date(), nullable=True))
    op.add_column('media_files', sa.Column('end_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('media_files', 'end_date')
    op.drop_column('media_files', 'start_date')
    # ### end Alembic commands ###
