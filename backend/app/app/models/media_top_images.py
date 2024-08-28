from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String,Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class MediaTopImages(Base):

    __tablename__ ="media_top_images"

    id=Column(Integer,primary_key=True)

    top_image = Column(String(500))
    top_url = Column(String(500))
    media_files_id = Column(Integer,ForeignKey("media_files.id")) 

    # default_img_path = Column(String(500))

    status=Column(TINYINT,comment="1->active,-1->deleted")
    created_at=Column(DateTime)
    media_files=relationship("MediaFiles",back_populates="media_top_images")


     
