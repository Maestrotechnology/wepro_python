from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Text,Date
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    id = Column(Integer,primary_key=True)
    user_type =Column(TINYINT,comment="1->SuperAdmin,2->Admin,3->Hr,4->Chief Editor,5->Sub Editor,6-Technical Lead,7->Digital Marketing strategist,8-journalist,,9-SEO-Google Strategist,10-Marketing,11-Web designer,12-Graphic Designer")

    name = Column(String(100))
    dob = Column(Date)
    user_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    joining_date = Column(Date)

    alternative_no = Column(String(20))
    whatsapp_no = Column(String(20))
    address = Column(Text)
    account_number = Column(String(255))
    pan_number = Column(String(255))
    aadhaar_number = Column(String(255))
    educational_qualification = Column(String(255))
    area_of_interest = Column(String(500))
    previous_experience = Column(String(500))
    experience_in_relevent_field = Column(String(500))
    past_designation = Column(String(500))
    bank = Column(String(255))
    ifsc_code = Column(String(255))
    branch = Column(String(500))
    request_user =Column(TINYINT,comment = "1->Yes,2->No")

    is_request =Column(TINYINT,comment = "1->Request,2-Accpted,3-Interview Process,-1 ->rejected")

    state_id = Column(Integer,ForeignKey("states.id")) 
    city_id = Column(Integer,ForeignKey("cities.id")) 
    approved_by = Column(Integer,ForeignKey("user.id")) 
    rejected_by = Column(Integer,ForeignKey("user.id")) 
    created_by = Column(Integer,ForeignKey("user.id")) 
    updated_by = Column(Integer,ForeignKey("user.id")) 
    pincode = Column(String(10))
    password = Column(String(255))
    is_active = Column(TINYINT,comment = "1->active,0->inactive")
    img_path =Column(String(255))
    img_alter = Column(String(255))
    reset_key=Column(String(255))
    otp = Column(String(10))
    resume_path = Column(Text)
    employment_type = Column(TINYINT,comment='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary,6-hyper')


    otp_expire_at = Column(DateTime)

    created_at=Column(DateTime)
    requested_at=Column(DateTime)
    approved_at=Column(DateTime)
    rejected_at=Column(DateTime)
    
    updated_at=Column(DateTime)
    status=Column(TINYINT,comment="-1->delete,1->active,0->inactive")

    api_tokens=relationship("ApiTokens",back_populates="user")
    article_files=relationship("ArticleFiles",back_populates="user")
    cities=relationship("Cities",back_populates="user")
    states=relationship("States",back_populates="user")
    email_history=relationship("EmailHistory",back_populates="user")
    journalist_approved_by = relationship('User', foreign_keys=[approved_by])
    journalist_rejected_by = relationship('User', foreign_keys=[rejected_by])
    user_acc_created_by = relationship('User', foreign_keys=[created_by])
    user_acc_updated_by = relationship('User', foreign_keys=[updated_by])

    




