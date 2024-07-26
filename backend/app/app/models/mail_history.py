from sqlalchemy import Column, Integer,Date, String, DateTime,DECIMAL, ForeignKey,Text
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class EmailHistory(Base):

    __tablename__="email_history"
    id = Column(Integer,primary_key=True)
    from_email = Column(String(255))
    to_email = Column(String(255))
    subject = Column(String(255))
    message = Column(String(255))
    response = Column(String(255))
    article_id = Column(Integer,ForeignKey("article.id"),comment="article tab id")
    user_id = Column(Integer,ForeignKey("user.id"),comment="user tab id")
    email_type=Column(TINYINT,comment="1->Journalist Account,2->Article,3->Forget Password,4->Reset Password,5-signup,6-Payment")


    created_at=Column(DateTime)


    status=Column(TINYINT,comment="-1->delete,1->active,0->inactive")
    article=relationship("Article",back_populates="email_history")
    user=relationship("User",back_populates="email_history")