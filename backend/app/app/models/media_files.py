from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String,Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class MediaFiles(Base):

    __tablename__ ="media_files"

    id=Column(Integer,primary_key=True)
    description=Column(String(250))
    title=Column(String(250))
    start_date=Column(Date)
    end_date=Column(Date)
    brand_name=Column(String(250))
    media_orientation =Column(TINYINT,comment="1->Portrait,2-Landscape")
    media_page =Column(TINYINT,comment="1->Home,2-Category")
    # is_google_ad =Column(TINYINT,comment="1->yes,0-No")
    media_position =Column(TINYINT,comment="1->Top,2-Bottom,3-right,4-Left")
    meta_title = Column(String(250))
    meta_description = Column(String(250))
    meta_keywords = Column(String(250))
    seo_url = Column(String(250))
    img_alter = Column(String(255))
    img_path = Column(String(500))

    top_image = Column(String(500))
    left_image = Column(String(500))
    right_image = Column(String(500))
    bottom_image = Column(String(500))

    top_url = Column(String(500))
    left_url = Column(String(500))
    right_url = Column(String(500))
    bottom_url = Column(String(500))


    # default_img_path = Column(String(500))
    content_type = Column(TINYINT,comment="1->Advertisement,2->Banners,3-youtube,4-shorts")
    media_type=Column(TINYINT,comment="1->images,2-shorts,3->Video")
    media_url = Column(String(500))

    status=Column(TINYINT,comment="1->active,-1->deleted")
    created_at=Column(DateTime)
    updated_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
    updated_by = Column(Integer,ForeignKey("user.id"),comment="user id")
     
    createdBy = relationship('User', foreign_keys=[created_by])
    updatedBy = relationship('User', foreign_keys=[updated_by])
