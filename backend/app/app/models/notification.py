from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class Notification(Base):
    __tablename__ ="notification"

    id=Column(Integer,primary_key=True)
    comment = Column(String(500))
    title = Column(String(500))
    article_id = Column(Integer,ForeignKey("article.id"),comment="article tab id")
    topic_id = Column(Integer,ForeignKey("article_topic.id"),comment="article topic id")
    user_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    admin_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    admin_notify = Column(TINYINT,comment="1->Notify,2->Read")
    journalist_notify = Column(TINYINT,comment="1->Notify,2->Read")
    topic_status = Column(TINYINT,comment="1->new,2-review,3-comment,4->approved")
    content_status = Column(TINYINT,comment="1->new,2-review,3-comment,4->approved")
    notification_type=Column(TINYINT,comment="1->topic,2-content,3-Requested Account,4->editors topic")
    status=Column(TINYINT,comment="1->active,-1->deleted")

    created_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
   
    createdBy = relationship('User', foreign_keys=[created_by])
    userRef = relationship('User', foreign_keys=[user_id])
    adminRef = relationship('User', foreign_keys=[admin_id])
    article=relationship("Article",back_populates="notification")
    article_topic=relationship("ArticleTopic",back_populates="notification")
    

