from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class Cities(Base):
    id=Column(Integer,primary_key=True)
    state_id=Column(Integer,ForeignKey("states.id"))
    name=Column(String(250))

    status=Column(TINYINT,comment="1->active,-1->deleted")

    
    states=relationship("States",back_populates="cities")
    user = relationship('User',back_populates="cities")
    article = relationship('Article',back_populates="cities")

