"""add file type in article files

Revision ID: e136c2274327
Revises: 9188f3646a58
Create Date: 2024-08-01 12:00:41.910480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e136c2274327'
down_revision: Union[str, None] = '9188f3646a58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_files', sa.Column('file_type', mysql.TINYINT(), nullable=True, comment='1->image,2 ->gif,3 ->pdf,4-> video,5 -> others'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article_files', 'file_type')
    # ### end Alembic commands ###
