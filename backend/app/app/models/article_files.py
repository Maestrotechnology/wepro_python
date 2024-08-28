from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer,ForeignKey,DECIMAL,Text,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base

class ArticleFiles(Base):
    __tablename__ ="article_files"
    id=Column(Integer,primary_key=True)
    img_path = Column(String(500))
    img_alter = Column (String(255))
    file_type =Column(TINYINT,comment="1->image,2 ->gif,3 ->pdf,4-> video,5 -> others")
    article_id = Column(Integer,ForeignKey("article.id"),comment="journal tab id")

    # is_top_image=Column(TINYINT,comment="1->yes")
    status=Column(TINYINT,comment="1->active,-1->deleted")
    created_at=Column(DateTime)

    created_by = Column(Integer,ForeignKey("user.id"),comment="user id")
   
    user=relationship("User",back_populates="article_files")
    article=relationship("Article",back_populates="article_files")
    

