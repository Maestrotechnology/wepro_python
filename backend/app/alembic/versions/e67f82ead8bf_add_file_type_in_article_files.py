"""add file type in article files

Revision ID: e67f82ead8bf
Revises: 76f1604405ac
Create Date: 2024-08-05 17:41:11.168854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e67f82ead8bf'
down_revision: Union[str, None] = '76f1604405ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('category', 'img_type',
               existing_type=mysql.TINYINT(),
               comment='1->png,0->jpg,3-jpeg',
               existing_comment='1->png,2->jpg,3-jpeg',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('category', 'img_type',
               existing_type=mysql.TINYINT(),
               comment='1->png,2->jpg,3-jpeg',
               existing_comment='1->png,0->jpg,3-jpeg',
               existing_nullable=True)
    # ### end Alembic commands ###
