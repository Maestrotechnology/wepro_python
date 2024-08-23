from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class ArticleHistory(Base):
    __tablename__ ="article_history"

    id=Column(Integer,primary_key=True)
    
    comment = Column(String(500))
    title = Column(String(500))
    article_id = Column(Integer,ForeignKey("article.id"),comment="article tab id")
    topic_id = Column(Integer,ForeignKey("article_topic.id"),comment="topic tab id")
    sub_editor_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    chief_editor_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    journalist_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    sub_editor_notify = Column(TINYINT,comment="1->Notify,2->Read")
    chief_editor_notify = Column(TINYINT,comment="1->Notify,2->Read")
    admin_notify = Column(TINYINT,comment="1->Notify,2->Read")
    journalist_notify = Column(TINYINT,comment="1->Notify,2->Read")
    topic_status = Column(TINYINT,comment="1->new,2-review,3-comment,4->approved")
    content_status = Column(TINYINT,comment="1->new,2-review,3-comment,4->approved")
    is_editor = Column(TINYINT,comment="1->Se,-2->Ce")
    history_type=Column(TINYINT,comment="1->topic,2-content,3-editors_topic")
    status=Column(TINYINT,comment="1->active,-1->deleted")

    created_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
   
    createdBy = relationship('User', foreign_keys=[created_by])
    subEditerUser = relationship('User', foreign_keys=[sub_editor_id])
    chiefEditerUser = relationship('User', foreign_keys=[chief_editor_id])
    journalistUser = relationship('User', foreign_keys=[journalist_id])
    article=relationship("Article",back_populates="article_history")
    article_topic=relationship("ArticleTopic",back_populates="article_history")
    

