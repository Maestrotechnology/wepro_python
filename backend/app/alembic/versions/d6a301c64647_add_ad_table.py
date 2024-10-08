"""add ad table

Revision ID: d6a301c64647
Revises: b7f5b40d3d72
Create Date: 2024-07-17 16:54:35.949905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd6a301c64647'
down_revision: Union[str, None] = 'b7f5b40d3d72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=500), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True, comment='article tab id'),
    sa.Column('sub_editor_id', sa.Integer(), nullable=True, comment='user id'),
    sa.Column('chief_editor_id', sa.Integer(), nullable=True, comment='user id'),
    sa.Column('journalist_id', sa.Integer(), nullable=True, comment='user id'),
    sa.Column('sub_editor_notify', mysql.TINYINT(), nullable=True, comment='1->Notify,2->Read'),
    sa.Column('chief_editor_notify', mysql.TINYINT(), nullable=True, comment='1->Notify,2->Read'),
    sa.Column('journalist_notify', mysql.TINYINT(), nullable=True, comment='1->Notify,2->Read'),
    sa.Column('status', mysql.TINYINT(), nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at.strftime("%Y-%m-%d %H:%M:%S")', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True, comment='user id'),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['chief_editor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['journalist_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sub_editor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('articlehistory')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articlehistory',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('comment', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('article_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='article tab id'),
    sa.Column('sub_editor_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('chief_editor_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('sub_editor_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('chief_editor_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('journalist_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at.strftime("%Y-%m-%d %H:%M:%S")', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('journalist_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], name='articlehistory_ibfk_1'),
    sa.ForeignKeyConstraint(['chief_editor_id'], ['user.id'], name='articlehistory_ibfk_2'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='articlehistory_ibfk_3'),
    sa.ForeignKeyConstraint(['journalist_id'], ['user.id'], name='articlehistory_ibfk_6'),
    sa.ForeignKeyConstraint(['sub_editor_id'], ['user.id'], name='articlehistory_ibfk_5'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('article_history')
    # ### end Alembic commands ###
