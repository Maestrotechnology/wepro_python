from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String,Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class Article(Base):

    id=Column(Integer,primary_key=True)
    content=Column(String(250))
    topic=Column(String(250))
    description=Column(String(250))
    topics=Column(String(250))
    img_alter = Column(String(250))
    meta_title = Column(String(250))
    meta_description = Column(String(250))
    meta_keywords = Column(String(250))
    submition_date = Column(Date)
    seo_url = Column(String(250))
    state_id = Column(Integer,ForeignKey("states.id")) 
    city_id = Column(Integer,ForeignKey("cities.id")) 
    category_id = Column(Integer,ForeignKey("category.id")) 
    sub_category_id = Column(Integer,ForeignKey("sub_category.id")) 
    comment = Column(String(500))
    topic_approved = Column(TINYINT,default=0,comment="0-not submitted,1->new,2->SE approved,3-CE Approved,4-On Hold")
    content_approved = Column(TINYINT,default=0,comment="0-not submitted,1->new,2->SE approved,3-CE Approved,4-On Hold")
    is_journalist = Column(TINYINT,comment="1-yes")
    sub_editor_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    chief_editor_id = Column(Integer,ForeignKey("user.id"),comment="user id")

    status=Column(TINYINT,comment="1->active,-1->deleted")
    created_at=Column(DateTime)
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



