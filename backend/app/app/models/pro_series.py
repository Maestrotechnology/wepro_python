from sqlalchemy import  Column, Integer,TEXT, DECIMAL,String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

from app.db.base_class import Base

class ProStories(Base):
    __tablename__ = "pro_stories"
    id=Column(Integer,primary_key=True)
    title=Column(String(500))
    img_path=Column(String(2000))
    url = Column(String(2000))
    series_type = Column(TINYINT,comment='1-Parent, 2-child')
    description=Column(TEXT)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)
    parent_id = Column(Integer,ForeignKey("pro_stories.id"),comment="pro_stories id")

    status=Column(TINYINT(1),comment="1-active, -1 inactive, 0- deleted")


    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
    updated_by = Column(Integer,ForeignKey("user.id"),comment="user id")
    parentStories = relationship('ProStories', foreign_keys=[parent_id])

     
    createdBy = relationship('User', foreign_keys=[created_by])
    updatedBy = relationship('User', foreign_keys=[updated_by])
  