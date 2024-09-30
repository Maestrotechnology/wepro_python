from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

from app.db.base_class import Base

class Ratings(Base):
    id=Column(Integer,primary_key=True)
    star =Column(Integer)
    amount = Column(Integer)
    updated_by = Column(Integer,ForeignKey("user.id"),comment="user id")

    status=Column(TINYINT(1),comment="1-active, -1 inactive, 0- deleted")
    article=relationship("Article",back_populates="ratings")

    updatedBy = relationship('User', foreign_keys=[updated_by])
