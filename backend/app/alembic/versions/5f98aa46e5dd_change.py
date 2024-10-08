"""change

Revision ID: 5f98aa46e5dd
Revises: 3932e6edb60b
Create Date: 2024-07-18 09:39:22.723168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5f98aa46e5dd'
down_revision: Union[str, None] = '3932e6edb60b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media_files', 'content_type',
               existing_type=mysql.TINYINT(),
               comment='1->Advertisement,2->Banners',
               existing_comment='1->Advertisement,2->others',
               existing_nullable=True)
    op.alter_column('media_files', 'media_type',
               existing_type=mysql.TINYINT(),
               comment='1->images,2-shorts,3->Video',
               existing_comment='1->shorts,2->Video',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media_files', 'media_type',
               existing_type=mysql.TINYINT(),
               comment='1->shorts,2->Video',
               existing_comment='1->images,2-shorts,3->Video',
               existing_nullable=True)
    op.alter_column('media_files', 'content_type',
               existing_type=mysql.TINYINT(),
               comment='1->Advertisement,2->others',
               existing_comment='1->Advertisement,2->Banners',
               existing_nullable=True)
    # ### end Alembic commands ###
