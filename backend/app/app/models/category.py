from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class Category(Base):

    id=Column(Integer,primary_key=True)
    description=Column(String(250))
    title=Column(String(250))
    img_alter=Column(String(250))
    img_path = Column(Text)
    sort_order = Column(Integer,comment="category order no")
    status=Column(TINYINT,comment="1->active,-1->deleted")
    created_at=Column(DateTime)
    updated_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
    updated_by = Column(Integer,ForeignKey("user.id"),comment="user id")
     
    createdBy = relationship('User', foreign_keys=[created_by])
    updatedBy = relationship('User', foreign_keys=[updated_by])
    sub_category =relationship("SubCategory",back_populates="category")

