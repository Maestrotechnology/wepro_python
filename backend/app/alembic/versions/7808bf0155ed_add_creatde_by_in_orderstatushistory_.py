"""add creatde by in OrderStatusHistory table

Revision ID: 7808bf0155ed
Revises: e569599a52dd
Create Date: 2024-08-28 18:04:56.257286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7808bf0155ed'
down_revision: Union[str, None] = 'e569599a52dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('email_history')
    # op.drop_table('article_topic')
    # op.drop_table('media_files')
    # op.drop_table('notification')
    # op.drop_table('article')
    # op.drop_table('cms_settings')
    # op.drop_table('media_top_images')
    # op.drop_table('article_history')
    # op.drop_table('article_files')
    # op.drop_table('brand_campaigns')
    # op.drop_table('careers')
    # ### end Alembic commands ###
    pass


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('careers',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('salary', mysql.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('employement_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary,6-hyper'),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('requirements', mysql.TEXT(), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('status', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='1-active, -1 inactive, 0- deleted'),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('updated_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('experience_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-fresher, 2-experience'),
    sa.Column('experience_year_from', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('experience_year_to', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('designation_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->SuperAdmin,2->Admin,3->Hr,4->Chief Editor,5->Sub Editor,6-Technical Lead,7->Digital Marketing strategist,8-journalist,,9-SEO-Google Strategist,10-Marketing,11-Web designer,12-Graphic Designer'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='careers_ibfk_1'),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], name='careers_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('brand_campaigns',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('title', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('img_alter', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('img_path', mysql.TEXT(), nullable=True),
    sa.Column('media_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->image,2->Gif'),
    sa.Column('brand_url', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('sort_order', mysql.INTEGER(), autoincrement=False, nullable=True, comment='brand campaigngs order no'),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('updated_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='brand_campaigns_ibfk_1'),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], name='brand_campaigns_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('article_files',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('img_path', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('img_alter', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('article_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='journal tab id'),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('file_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->image,2 ->gif,3 ->pdf,4-> video,5 -> others'),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], name='article_files_ibfk_1'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='article_files_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('article_history',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('comment', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('article_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='article tab id'),
    sa.Column('sub_editor_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('chief_editor_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('journalist_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('sub_editor_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('chief_editor_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('journalist_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('topic_status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->new,2-review,3-comment,4->approved'),
    sa.Column('content_status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->new,2-review,3-comment,4->approved'),
    sa.Column('is_editor', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Se,-2->Ce'),
    sa.Column('history_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->topic,2-content,3-editors_topic'),
    sa.Column('admin_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('topic_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='topic tab id'),
    sa.Column('title', mysql.VARCHAR(length=500), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], name='article_history_ibfk_1'),
    sa.ForeignKeyConstraint(['chief_editor_id'], ['user.id'], name='article_history_ibfk_2'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='article_history_ibfk_3'),
    sa.ForeignKeyConstraint(['journalist_id'], ['user.id'], name='article_history_ibfk_4'),
    sa.ForeignKeyConstraint(['sub_editor_id'], ['user.id'], name='article_history_ibfk_5'),
    sa.ForeignKeyConstraint(['topic_id'], ['article_topic.id'], name='article_history_ibfk_6'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('media_top_images',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('top_image', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('top_url', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('media_files_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['media_files_id'], ['media_files.id'], name='media_top_images_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('cms_settings',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('google_play', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('app_store', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('facebook', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('threads', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('linkedin', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('instagram', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('youtube', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('updated_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='-1->delete,1->active,0->inactive'),
    sa.Column('twitter', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('wepro_text', mysql.TEXT(), nullable=True),
    sa.Column('about', mysql.TEXT(), nullable=True),
    sa.Column('our_teams', mysql.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='cms_settings_ibfk_1'),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], name='cms_settings_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('article',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('topic', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('meta_title', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('meta_description', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('meta_keywords', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('submition_date', sa.DATE(), nullable=True),
    sa.Column('seo_url', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('comment', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('topic_approved', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->new,2-review,3-comment,4->CE Approved'),
    sa.Column('content_approved', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->new,2-review,3-comment,4->-Published(CE Approved)'),
    sa.Column('sub_editor_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('chief_editor_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('updated_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('category_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sub_category_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_journalist', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-yes'),
    sa.Column('description', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('state_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('city_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('img_alter', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('article_topic_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_paid', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-pending,2-Paid'),
    sa.Column('editors_choice', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->No,2->yes'),
    sa.Column('article_title', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('published_at', mysql.DATETIME(), nullable=True),
    sa.Column('img_path', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('footer_content', mysql.TEXT(), nullable=True),
    sa.Column('header_content', mysql.TEXT(), nullable=True),
    sa.Column('middle_content', mysql.TEXT(), nullable=True),
    sa.Column('youtube_link', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('content_created_at', mysql.DATETIME(), nullable=True),
    sa.Column('topic_se_approved_at', mysql.DATETIME(), nullable=True),
    sa.Column('content_se_approved_at', mysql.DATETIME(), nullable=True),
    sa.Column('topic_se_review_at', mysql.DATETIME(), nullable=True),
    sa.Column('topic_ce_review_at', mysql.DATETIME(), nullable=True),
    sa.Column('topic_ce_cmnt_at', mysql.DATETIME(), nullable=True),
    sa.Column('topic_se_cmnt_at', mysql.DATETIME(), nullable=True),
    sa.Column('topic_ce_approved_at', mysql.DATETIME(), nullable=True),
    sa.Column('content_se_review_at', mysql.DATETIME(), nullable=True),
    sa.Column('content_ce_review_at', mysql.DATETIME(), nullable=True),
    sa.Column('content_ce_cmnt_at', mysql.DATETIME(), nullable=True),
    sa.Column('content_se_cmnt_at', mysql.DATETIME(), nullable=True),
    sa.Column('topic_se_approved', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->new,2-review,3-comment,4->SE approved'),
    sa.Column('content_se_approved', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->new,2-review,3-comment,4->SE approved'),
    sa.Column('paid_amount', mysql.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('save_for_later', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->yes'),
    sa.Column('header_image', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('middle_image', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('se_header_checkbox', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-checked'),
    sa.Column('se_middle_checkbox', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-checked'),
    sa.Column('se_footer_checkbox', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-checked'),
    sa.Column('ce_header_checkbox', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-checked'),
    sa.Column('ce_middle_checkbox', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-checked'),
    sa.Column('ce_footer_checkbox', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1-checked'),
    sa.ForeignKeyConstraint(['article_topic_id'], ['article_topic.id'], name='article_ibfk_11'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name='article_ibfk_8'),
    sa.ForeignKeyConstraint(['chief_editor_id'], ['user.id'], name='article_ibfk_1'),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], name='article_ibfk_10'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='article_ibfk_3'),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], name='article_ibfk_9'),
    sa.ForeignKeyConstraint(['sub_category_id'], ['sub_category.id'], name='article_ibfk_7'),
    sa.ForeignKeyConstraint(['sub_editor_id'], ['user.id'], name='article_ibfk_5'),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], name='article_ibfk_6'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('notification',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('comment', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('article_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='article tab id'),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('admin_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('admin_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('journalist_notify', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Notify,2->Read'),
    sa.Column('topic_status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->new,2-review,3-comment,4->approved'),
    sa.Column('content_status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->new,2-review,3-comment,4->approved'),
    sa.Column('notification_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->topic,2-content,3-Requested Account,4->editors topic'),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('topic_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='article topic id'),
    sa.Column('title', mysql.VARCHAR(length=500), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['user.id'], name='notification_ibfk_1'),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], name='notification_ibfk_2'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='notification_ibfk_3'),
    sa.ForeignKeyConstraint(['topic_id'], ['article_topic.id'], name='notification_ibfk_5'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='notification_ibfk_4'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('media_files',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('title', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('meta_title', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('meta_description', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('meta_keywords', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('seo_url', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('img_alter', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('content_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Advertisement,2->Banners,3-youtube,4-shorts'),
    sa.Column('media_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->images,2-shorts,3->Video'),
    sa.Column('media_url', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('updated_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('img_path', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('media_orientation', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Portrait,2-Landscape'),
    sa.Column('media_position', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Top,2-Bottom,3-right,4-Left'),
    sa.Column('media_page', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Home,2-Category'),
    sa.Column('top_image', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('left_image', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('right_image', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('bottom_image', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('top_url', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('left_url', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('right_url', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('bottom_url', mysql.VARCHAR(length=500), nullable=True),
    sa.Column('brand_name', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('start_date', sa.DATE(), nullable=True),
    sa.Column('end_date', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='media_files_ibfk_1'),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], name='media_files_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('article_topic',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('topic', mysql.VARCHAR(length=250), nullable=True),
    sa.Column('category_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->active,-1->deleted'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('created_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('updated_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.Column('sub_category_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('is_choosed', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->yes'),
    sa.Column('is_approved', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->no,2-yes'),
    sa.Column('approved_by', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user id'),
    sa.ForeignKeyConstraint(['approved_by'], ['user.id'], name='article_topic_ibfk_5'),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name='article_topic_ibfk_1'),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='article_topic_ibfk_2'),
    sa.ForeignKeyConstraint(['sub_category_id'], ['sub_category.id'], name='article_topic_ibfk_4'),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], name='article_topic_ibfk_3'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('email_history',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('from_email', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('to_email', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('subject', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('message', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('response', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('article_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='article tab id'),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('status', mysql.TINYINT(), autoincrement=False, nullable=True, comment='-1->delete,1->active,0->inactive'),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True, comment='user tab id'),
    sa.Column('email_type', mysql.TINYINT(), autoincrement=False, nullable=True, comment='1->Journalist Account,2->Article,3->Forget Password,4->Reset Password,5-signup,6-Payment'),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], name='email_history_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='email_history_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
