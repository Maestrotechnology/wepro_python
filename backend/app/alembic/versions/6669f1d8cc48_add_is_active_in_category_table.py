"""add is_active in category table

Revision ID: 6669f1d8cc48
Revises: 7668194d8f00
Create Date: 2024-07-31 10:16:13.068778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '6669f1d8cc48'
down_revision: Union[str, None] = '7668194d8f00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media_files', 'content_type',
               existing_type=mysql.TINYINT(),
               comment='1->Advertisement,2->Banners,3-youtube',
               existing_comment='1->Advertisement,2->Banners,3-youtupe',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media_files', 'content_type',
               existing_type=mysql.TINYINT(),
               comment='1->Advertisement,2->Banners,3-youtupe',
               existing_comment='1->Advertisement,2->Banners,3-youtube',
               existing_nullable=True)
    # ### end Alembic commands ###
