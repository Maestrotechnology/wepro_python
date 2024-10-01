from sqlalchemy import Column, Integer,Date, String, DateTime,DECIMAL, ForeignKey,Text
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class WebsiteForms(Base):

    __tablename__="website_forms"
    id = Column(Integer,primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(255))
    company_name = Column(String(255))
    company_location = Column(String(255))
    subject = Column(String(255))
    message = Column(Text)
    service_type=Column(TINYINT,comment="6-Payment")
    form_type=Column(TINYINT,comment=" 	1 -> AD/Brand form, 2 -> contact form 3 -> newsletter 	")
    status=Column(TINYINT,comment="1-active")


    created_at=Column(DateTime)
    updated_at=Column(DateTime)

