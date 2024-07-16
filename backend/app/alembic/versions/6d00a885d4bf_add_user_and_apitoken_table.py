"""add user and apitoken table

Revision ID: 6d00a885d4bf
Revises: d25667f60b73
Create Date: 2024-07-16 14:14:40.009721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '6d00a885d4bf'
down_revision: Union[str, None] = 'd25667f60b73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('google_play', sa.String(length=255), nullable=True),
    sa.Column('app_store', sa.String(length=255), nullable=True),
    sa.Column('facebook', sa.String(length=255), nullable=True),
    sa.Column('threads', sa.String(length=255), nullable=True),
    sa.Column('linkedin', sa.String(length=255), nullable=True),
    sa.Column('instagram', sa.String(length=255), nullable=True),
    sa.Column('youtube', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True, comment='user id'),
    sa.Column('updated_by', sa.Integer(), nullable=True, comment='user id'),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='-1->delete,1->active,0->inactive'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_settings')
    # ### end Alembic commands ###
