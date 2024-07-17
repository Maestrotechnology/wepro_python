from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class States(Base):
    id=Column(Integer,primary_key=True)
    name=Column(String(250))
    status=Column(TINYINT,comment="1->active,-1->deleted")

    cities=relationship("Cities",back_populates="states")
    user = relationship('User',back_populates='states')
    article = relationship('Article',back_populates='states')


