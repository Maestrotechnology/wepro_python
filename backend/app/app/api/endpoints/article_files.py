from fastapi import APIRouter, Depends, Form,requests,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from datetime import datetime
from app.utils import *
from typing import List, Optional

router = APIRouter()

@router.post("/upload_article_file")
async def uploadFile(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     article_id: int = Form(...),
                     img_alter: str = Form(None),
                     upload_file: Optional[List[UploadFile]] = File(None),
                    
                     ):
    user = deps.get_user_token(db=db,token=token)
    if user:
        checkArticle = db.query(Article).filter(
            Article.id == article_id,Article.status == 1 ).first()
        

        file_type_map = {
        "image": ["image/jpeg", "image/png"],

        "gif": ["image/gif"],
        "pdf": ["application/pdf"],
        "video": ["video/mp4", "video/mpeg"],
    }
        
        file_type_int_map = {
            "image": 1,
            "gif": 2,
            "pdf": 3,
            "video": 4,
            "other": 5
        }
        if not checkArticle:
            return {"status":0,"msg":"No Article record found."}
        else:
            if upload_file:
                row = 0
                imageData =[]
                for file in upload_file:
                    uploadedFile = file.filename
                    fName,*etn = uploadedFile.split(".")
                    filePath,returnFilePath = file_storage(file,fName)

                    splited_filename = img_alter.split(',') if img_alter else None


                    file_type = file_type_int_map["other"]  # Default to 'other' if type is not recognized
                    content_type = file.content_type.lower()

                    # Check for GIF first
                    if content_type in file_type_map["gif"]:
                        file_type = file_type_int_map["gif"]
                    else:
                        for key, values in file_type_map.items():
                            # if key != "gif" and any(content_type.startswith(value.split('/')[0]) for value in values):
                            if key != "gif" and content_type in values:
                                file_type = file_type_int_map[key]
                                break

                    

                    imageData.append({
                        "img_path" : returnFilePath,
                        "img_alter" : img_alter,
                        "created_at" : datetime.now(settings.tz_IN),
                        "status" : 1,
                        "file_type":file_type,
                        "article_id":article_id,
                        "created_by":user.id
                    })
                    # print(returnFilePath)
                    row += 1
                
                try:
                    with db as conn:
                        conn.execute(ArticleFiles.__table__.insert().values(imageData))
                        conn.commit()
                    return({"status": 1,"msg": "Uploaded Successfully."})
                
                except Exception as e:
                    
                    print(f"Error during bulk insert: {str(e)}")
                    return {"status": 0,"msg": "Failed to insert image"}

            else:
                return {"status": 0,"msg": "No file is selected."}
    else:
        return {"status":-1,"msg":"Sorry your login session expires.Please login again."}


@router.post("/list_article_files")
async def listArticleFiles(db:Session = Depends(deps.get_db),
                        token:str = Form(...),article_id:int=Form(None)):
    user = deps.get_user_token(db=db,token=token)
    if  user:
        getAllArticleFiles = db.query(ArticleFiles).filter(ArticleFiles.status == 1)
        if article_id:
            getAllArticleFiles = getAllArticleFiles.filter(ArticleFiles.article_id == article_id)
    
        getAllArticleFiles = getAllArticleFiles.order_by(ArticleFiles.id.desc())

        attachmentCount = getAllArticleFiles.count()
       
        getAllArticleFiles = getAllArticleFiles.all()

        dataList = []
        if getAllArticleFiles:
            for row in getAllArticleFiles:
                dataList.append({
                    "article_file_id":row.id,
                    "alter_img":row.img_alter,
                    "file_type":row.file_type,
                    "img_path": f"{settings.BASE_DOMAIN}{row.img_path}",
                })
        data=({
               "total_count": attachmentCount,"items": dataList})
        return {"status": 1,"msg": "success","data": data}
    else:
        return {"status":-1,"msg":"Sorry your login session expires.Please login again."}

@router.post("/delete_article_file")
async def deleteAttachments(db: Session = Depends(deps.get_db),
                            token:str = Form(...),
                            article_file_id: int = Form(...)):
    user = deps.get_user_token(db=db,token=token)
    
    if  user:
        deleteAttachment = db.query(ArticleFiles).filter(
            ArticleFiles.id == article_file_id,
            ArticleFiles.status == 1
        ).first()
        deleteAttachment.status=-1
        db.commit()
        file_path = deleteAttachment.img_path
        
        file_loc = settings.BASE_UPLOAD_FOLDER+"/"+file_path

        if os.path.exists(file_loc):
            os.remove(file_loc)
        return {"status": 1,"msg": "ArticleFiles deleted successfully"}
    return {"status":-1,"msg":"Sorry your login session expires.Please login again."}



