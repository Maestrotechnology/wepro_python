"""change

Revision ID: 55f2ffb98026
Revises: 5f98aa46e5dd
Create Date: 2024-07-18 12:46:37.414628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '55f2ffb98026'
down_revision: Union[str, None] = '5f98aa46e5dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_request', mysql.TINYINT(), nullable=True, comment='1->Accepted,0->Request,-1 ->rejected'))
    op.drop_column('user', 'approval_status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('approval_status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Accepted,0->Request,-1 ->rejected'))
    op.drop_column('user', 'is_request')
    # ### end Alembic commands ###
