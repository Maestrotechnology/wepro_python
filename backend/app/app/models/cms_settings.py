from sqlalchemy import Column, Integer,Date, String, DateTime,DECIMAL, ForeignKey,Text
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class CmsSettings(Base):

    __tablename__="cms_settings"
    id = Column(Integer,primary_key=True)
    google_play = Column(String(255))
    app_store = Column(String(255))
    facebook = Column(String(255))
    threads = Column(String(255))
    twitter = Column(String(255))
    linkedin = Column(String(255))
    instagram = Column(String(255))
    youtube = Column(String(255))
    wepro_text = Column(Text)
    about = Column(Text)
    our_teams = Column(Text)

    created_at=Column(DateTime)
    updated_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
    updated_by = Column(Integer,ForeignKey("user.id"),comment="user id")
        # user = relationship("User",back_populates="quotation")
    createdBy = relationship('User', foreign_keys=[created_by])
    updatedBy = relationship('User', foreign_keys=[updated_by])

    status=Column(TINYINT,comment="-1->delete,1->active,0->inactive")