from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class ArticleHistory(Base):
    __tablename__ ="article_history"

    id=Column(Integer,primary_key=True)
    comment = Column(String(500))
    article_id = Column(Integer,ForeignKey("article.id"),comment="article tab id")
    sub_editor_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    chief_editor_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    journalist_id = Column(Integer,ForeignKey("user.id"),comment="user id")
    sub_editor_notify = Column(TINYINT,comment="1->Notify,2->Read")
    chief_editor_notify = Column(TINYINT,comment="1->Notify,2->Read")
    journalist_notify = Column(TINYINT,comment="1->Notify,2->Read")
    topic_status = Column(TINYINT,default=1,comment="1->new,2-review,3-comment,4->SE approved,5-CE Approved")
    content_status = Column(TINYINT,default=1,comment="1->new,2-review,3-comment,4->SE approved,5-Published(CE Approved)")
  
    is_topic=Column(TINYINT,comment="1->yes")
    is_content=Column(TINYINT,comment="1->yes")
    status=Column(TINYINT,comment="1->active,-1->deleted")

    created_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
   
    createdBy = relationship('User', foreign_keys=[created_by])
    subEditerUser = relationship('User', foreign_keys=[sub_editor_id])
    chiefEditerUser = relationship('User', foreign_keys=[chief_editor_id])
    journalistUser = relationship('User', foreign_keys=[journalist_id])
    article=relationship("Article",back_populates="article_history")
    

