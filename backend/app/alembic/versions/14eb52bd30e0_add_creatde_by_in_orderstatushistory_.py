"""add creatde by in OrderStatusHistory table

Revision ID: 14eb52bd30e0
Revises: 87ed6aabe6c9
Create Date: 2024-08-28 10:12:06.102705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '14eb52bd30e0'
down_revision: Union[str, None] = '87ed6aabe6c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media_top_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('top_image', sa.String(length=500), nullable=True),
    sa.Column('top_url', sa.String(length=500), nullable=True),
    sa.Column('media_files_id', sa.Integer(), nullable=True),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['media_files_id'], ['media_files.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media_top_images')
    # ### end Alembic commands ###
