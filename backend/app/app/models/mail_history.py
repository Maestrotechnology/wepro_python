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
    journal_id = Column(Integer,ForeignKey("journal.id"),comment="journal tab id")

    created_at=Column(DateTime)


    status=Column(TINYINT,comment="-1->delete,1->active,0->inactive")
    journal=relationship("journal",back_populates="email_history")
    user=relationship("User",back_populates="email_history")