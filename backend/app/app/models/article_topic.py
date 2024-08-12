from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class ArticleTopic(Base):

    __tablename__ = "article_topic"

    id=Column(Integer,primary_key=True)
    description=Column(String(250))
    topic=Column(String(250))
    category_id = Column(Integer,ForeignKey("category.id")) 
    sub_category_id = Column(Integer,ForeignKey("sub_category.id")) 

    status=Column(TINYINT,comment="1->active,-1->deleted")
    created_at=Column(DateTime)
    updated_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
    updated_by = Column(Integer,ForeignKey("user.id"),comment="user id")
     
    createdBy = relationship('User', foreign_keys=[created_by])
    updatedBy = relationship('User', foreign_keys=[updated_by])
    category=relationship("Category",back_populates="article_topic")
    sub_category=relationship("SubCategory",back_populates="article_topic")
    article=relationship("Article",back_populates="article_topic")

