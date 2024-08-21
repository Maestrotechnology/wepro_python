"""add creatde by in OrderStatusHistory table

Revision ID: 372a307d22a7
Revises: 99efd316831e
Create Date: 2024-08-21 12:12:25.756272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '372a307d22a7'
down_revision: Union[str, None] = '99efd316831e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_topic', sa.Column('is_choosed', mysql.TINYINT(), nullable=True, comment='1->yes'))
    op.alter_column('media_files', 'media_orientation',
               existing_type=mysql.TINYINT(),
               comment='1->Portrait,2-Landscape',
               existing_comment='1->vertical,2-horizontal',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media_files', 'media_orientation',
               existing_type=mysql.TINYINT(),
               comment='1->vertical,2-horizontal',
               existing_comment='1->Portrait,2-Landscape',
               existing_nullable=True)
    op.drop_column('article_topic', 'is_choosed')
    # ### end Alembic commands ###
