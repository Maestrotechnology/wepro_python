from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class Journal(Base):

    id=Column(Integer,primary_key=True)
    content=Column(String(250))
    topic=Column(String(250))
    meta_title = Column(String(250))
    meta_description = Column(String(250))
    meta_keywords = Column(String(250))
    seo_url = Column(String(250))
    state_id = Column(Integer,ForeignKey("states.id")) 
    city_id = Column(Integer,ForeignKey("cities.id")) 
    media_path = Column(String(500))
    comment = Column(String(500))
    topic_approved = Column(TINYINT,comment="0->waiting,1->SE approved,2-CE Approved")
    content_approved = Column(TINYINT,comment="0->waiting,1->SE approved,2-CE Approved")
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
    cities=relationship("Cities",back_populates="journal")
    states=relationship("States",back_populates="journal")
    journal_files=relationship("JournalFiles",back_populates="journal")
    email_history=relationship("EmailHistory",back_populates="journal")

