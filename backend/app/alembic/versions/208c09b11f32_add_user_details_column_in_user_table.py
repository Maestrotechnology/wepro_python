"""add user details  column in user table

Revision ID: 208c09b11f32
Revises: 70c249802f19
Create Date: 2024-07-26 14:44:24.629036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '208c09b11f32'
down_revision: Union[str, None] = '70c249802f19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('rejected_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'user', ['rejected_by'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'rejected_by')
    # ### end Alembic commands ###
