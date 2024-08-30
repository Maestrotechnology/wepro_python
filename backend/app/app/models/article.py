from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String,Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class Article(Base):

    id=Column(Integer,primary_key=True)
    content=Column(String(250))
    topic=Column(String(250))
    article_title=Column(String(500))
    youtube_link=Column(String(500))
    img_path = Column(String(500))
    header_image = Column(String(500))
    middle_image = Column(String(500))
    description=Column(String(2000))

    footer_content = Column(Text)
    header_content = Column(Text)
    middle_content = Column(Text)
    is_paid = Column(TINYINT,default=1,comment="1-pending,2-Paid")
    paid_amount=Column(DECIMAL(10,2))
    se_header_checkbox = Column(TINYINT,default=0,comment="1-checked")
    se_middle_checkbox = Column(TINYINT,default=0,comment="1-checked")
    se_footer_checkbox = Column(TINYINT,default=0,comment="1-checked")
    ce_header_checkbox = Column(TINYINT,default=0,comment="1-checked")
    ce_middle_checkbox = Column(TINYINT,default=0,comment="1-checked")
    ce_footer_checkbox = Column(TINYINT,default=0,comment="1-checked")

    img_alter = Column(String(250))
    meta_title = Column(String(250))
    meta_description = Column(String(250))
    meta_keywords = Column(String(250))
    submition_date = Column(Date)
    seo_url = Column(String(250))
    state_id = Column(Integer,ForeignKey("states.id")) 
    article_topic_id = Column(Integer,ForeignKey("article_topic.id")) 
    city_id = Column(Integer,ForeignKey("cities.id")) 
    category_id = Column(Integer,ForeignKey("category.id")) 
    sub_category_id = Column(Integer,ForeignKey("sub_category.id")) 
    comment = Column(String(500))
    topic_approved = Column(TINYINT,comment="1->new,2-review,3-comment,4->CE Approved")
    content_approved = Column(TINYINT,comment="1->new,2-review,3-comment,4->-Published(CE Approved)")
    topic_se_approved = Column(TINYINT,default=1,comment="1->new,2-review,3-comment,4->SE approved")
    content_se_approved = Column(TINYINT,comment="1->new,2-review,3-comment,4->SE approved")
    is_journalist = Column(TINYINT,comment="1-yes")
    sub_editor_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    chief_editor_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    editors_choice = Column(TINYINT,default=1,comment="1->No,2->yes")

    status=Column(TINYINT,comment="1->active,-1->deleted")
    save_for_later=Column(TINYINT,default=0,comment="1->yes")

    created_at=Column(DateTime)
    content_created_at=Column(DateTime)


    topic_se_review_at=Column(DateTime)
    topic_ce_review_at=Column(DateTime)

    topic_ce_cmnt_at=Column(DateTime)
    topic_se_cmnt_at=Column(DateTime)

    topic_se_approved_at=Column(DateTime)
    topic_ce_approved_at=Column(DateTime)

    content_se_review_at=Column(DateTime)
    content_ce_review_at=Column(DateTime)

    content_ce_cmnt_at=Column(DateTime)
    content_se_cmnt_at=Column(DateTime)
   
    content_se_approved_at=Column(DateTime)
    published_at=Column(DateTime)

    updated_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
    updated_by = Column(Integer,ForeignKey("user.id"),comment="user id")
     
    createdBy = relationship('User', foreign_keys=[created_by])
    subEditerUser = relationship('User', foreign_keys=[sub_editor_id])
    chiefEditerUser = relationship('User', foreign_keys=[chief_editor_id])
    updatedBy = relationship('User', foreign_keys=[updated_by])
    cities=relationship("Cities",back_populates="article")
    states=relationship("States",back_populates="article")
    article_files=relationship("ArticleFiles",back_populates="article")
    email_history=relationship("EmailHistory",back_populates="article")
    article_history=relationship("ArticleHistory",back_populates="article")
    category=relationship("Category",back_populates="article")
    sub_category=relationship("SubCategory",back_populates="article")
    article_topic=relationship("ArticleTopic",back_populates="article")
    notification=relationship("Notification",back_populates="article")



