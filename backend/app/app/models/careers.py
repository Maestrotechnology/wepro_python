from sqlalchemy import  Column, Integer,TEXT, DECIMAL,String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

from app.db.base_class import Base

class Careers(Base):
    __tablename__ = "careers"
    id=Column(Integer,primary_key=True)
    title=Column(String(250))
    salary = Column(DECIMAL(12,2),default=0)
    employement_type = Column(TINYINT,comment='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary,6-hyper')
    experience_type = Column(TINYINT,comment='1-fresher, 2-experience')
    designation_type =Column(TINYINT,comment="1->SuperAdmin,2->Admin,3->Hr,4->Chief Editor,5->Sub Editor,6-Technical Lead,7->Digital Marketing strategist,8-journalist,,9-SEO-Google Strategist,10-Marketing,11-Web designer,12-Graphic Designer")

    experience_year_from = Column(String(255))
    experience_year_to = Column(String(255))
    description=Column(TEXT)
    requirements=Column(TEXT)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)
    status=Column(TINYINT(1),comment="1-active, -1 inactive, 0- deleted")


    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
    updated_by = Column(Integer,ForeignKey("user.id"),comment="user id")
     
    createdBy = relationship('User', foreign_keys=[created_by])
    updatedBy = relationship('User', foreign_keys=[updated_by])
  