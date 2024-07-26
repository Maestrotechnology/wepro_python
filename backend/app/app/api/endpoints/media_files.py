from fastapi import APIRouter, Depends, Form,requests,UploadFile,File
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_,and_
from app.core import security
from datetime import datetime,timedelta,date
from typing import List, Optional,Dict



router = APIRouter()


@router.post("/create_media_files")
async def createMediaFiles(db:Session = Depends(deps.get_db),
                     media_url:str=Form(None),
                     title:str=Form(None),
                     description:str=Form(None),
                     meta_title:str=Form(None),
                     meta_description:str=Form(None),
                     img_alter:str=Form(None),
                     meta_keywords:str=Form(None),
                    #  seo_url:str=Form(None),
                     media_file:Optional[UploadFile] = File(None),

                     token:str=Form(...),
                     content_type:int=Form(None,description="1->Ads,2->banners"),
                     media_type:int=Form(None,description="1->img,2-shorts,3->Video")
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,7]:

            addCsmSettings = MediaFiles(media_url = media_url,
            title = title,
            description = description,
            meta_title = meta_title,
            media_type = media_type,
            img_alter = img_alter,
            content_type = content_type,
            meta_description = meta_description,
            # seo_url = seo_url,
            meta_keywords = meta_keywords,
            status=1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addCsmSettings)
            db.commit()

            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                addCsmSettings.img_path = returnFilePath

                db.commit()

            return {"status":1,"msg":"Successfully Cms Settings Created"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Cms Settings."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_media_files")
async def updateMediaFiles(db:Session = Depends(deps.get_db),
                     media_files_id:int=Form(...),
                     media_url:str=Form(None),
                     title:str=Form(None),
                     description:str=Form(None),
                     meta_title:str=Form(None),
                     img_alter:str=Form(None),
                     meta_description:str=Form(None),
                     meta_keywords:str=Form(None),
                     media_file:Optional[UploadFile] = File(None),

                    #  seo_url:str=Form(None),
                     token:str=Form(...)
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,7]:

            getMediaFiles = db.query(MediaFiles).filter(MediaFiles.id==media_files_id).first()

            if not getMediaFiles:
                return{"status":0,"msg":"Not Found"}
            
            getMediaFiles.media_url = media_url
            getMediaFiles.title = title
            getMediaFiles.img_alter = img_alter

            getMediaFiles.description = description
            getMediaFiles.meta_title = meta_title
            getMediaFiles.meta_description = meta_description
            # getMediaFiles.seo_url = seo_url
            getMediaFiles.meta_keywords = meta_keywords
            getMediaFiles.updated_at = datetime.now(settings.tz_IN)
            getMediaFiles.updated_by = user.id

            db.commit()

            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                getMediaFiles.img_path = returnFilePath

                db.commit()


            return {"status":1,"msg":"Successfully Cms Settings Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Cms Settings."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/list_media_files")
async def listMediaFiles(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       media_type:int=Form(None),
                       title:int=Form(None),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllAds = db.query(MediaFiles).filter(MediaFiles.status ==1)

            if media_type:
                getAllAds = getAllAds.filter(MediaFiles.media_type==media_type)
            if title:
                getAllAds =  getAllAds.filter(MediaFiles.title.like("%"+title+"%"))

            totalCount = getAllAds.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllAds = getAllAds.limit(limit).offset(offset).all()

            dataList=[]
            if getAllAds:
                for row in getAllAds:
                    dataList.append({
                "media_files_id":row.id,
                "media_url":row.media_url,
                "title":row.title,
                "description":row.description,
                "meta_title":row.meta_title,
                "meta_description":row.meta_description,
                # "seo_url":row.seo_url,
                "img_alter":row.img_alter,
                "media_file":f"{settings.BASE_DOMAIN}{row.img_path}" if row.img_path else "",
                "media_type":row.media_type,
                "content_type":row.content_type,
                "meta_keywords":row.meta_keywords,
                "created_at":row.created_at,                  
                "updated_at":row.updated_at,                  
                "created_by":row.createdBy.user_name if row.created_by else None,                  
                "updated_by":row.updatedBy.user_name if row.updated_by else None,                  
                      }  )
            
            data=({"page":page,"size":size,
                   "total_page":totalPages,
                   "total_count":totalCount,
                   "items":dataList})
        
            return ({"status":1,"msg":"Success","data":data})
        else:
            return {'status':0,"msg":"You are not authenticated to view media_files."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
    
@router.post("/view_media_files")
async def viewMediaFiles(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   media_files_id:int=Form(...),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
            
        getData = db.query(MediaFiles).filter(
            MediaFiles.status==1,MediaFiles.id==media_files_id).first()
        
        if not getData:
            return {"status":0,"msg":"No Record Found"}

        data={
            "media_files_id":getData.id,
            "media_url":getData.media_url,
            "title":getData.title,
            "media_file":f"{settings.BASE_DOMAIN}{getData.img_path}" if getData.img_path else "",

            "description":getData.description,
            "img_alter":getData.img_alter,
            "meta_title":getData.meta_title,
            "meta_description":getData.meta_description,
            # "seo_url":getData.seo_url,
            "media_type":getData.media_type,
            "content_type":getData.content_type,
            "meta_keywords":getData.meta_keywords,
            "created_at":getData.created_at,                  
            "updated_at":getData.updated_at,                  
            "created_by":getData.createdBy.user_name if getData.created_by else None,                  
            "updated_by":getData.updatedBy.user_name if getData.updated_by else None,                  
            }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/delete_media_files")
async def deleteMediaFiles(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     media_files_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,6] :
            getMediaFiles = db.query(MediaFiles).filter(MediaFiles.id == media_files_id,
                                            MediaFiles.status == 1)
            
            getMediaFiles = getMediaFiles.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"MediaFiles successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete any media_files"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}