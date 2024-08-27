from fastapi import APIRouter, Depends, Form,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from datetime import datetime,date
from app.utils import *
from datetime import datetime
from typing import Optional



router = APIRouter()


@router.post("/create_media_files")
async def createMediaFiles(db:Session = Depends(deps.get_db),
                     media_url:str=Form(...),
                     title:str=Form(None),
                     description:str=Form(None),
                     meta_title:str=Form(None),
                     meta_description:str=Form(None),
                     start_date:date=Form(None),
                     end_date:date=Form(None),
                     img_alter:str=Form(None),
                     meta_keywords:str=Form(None),
                    #  seo_url:str=Form(None),
                     media_file:Optional[UploadFile] = File(None),
                     top_url:Optional[UploadFile] = File(None),
                     bottom_url:Optional[UploadFile] = File(None),
                     right_url:Optional[UploadFile] = File(None),
                     left_url:Optional[UploadFile] = File(None),
                     media_orientation:int=Form(None,description="1->Portrait,2-Landscape"),
                     media_page:int=Form(None,description="1->Home,2-Category"),
                     top_image:Optional[UploadFile] = File(None),
                     bottom_image:Optional[UploadFile] = File(None),
                     right_image:Optional[UploadFile] = File(None),
                     left_image:Optional[UploadFile] = File(None),
                     brand_name:str=Form(None),
                     media_position:int=Form(None,description="1->Top,2-Bottom,3-right,4-Left"),
                     token:str=Form(...),
                     content_type:int=Form(None,description="1->Ads,2->banners,3-youtube"),
                     media_type:int=Form(None,description="1->img,2-shorts,3->Video")
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,7]:

            existUrl =db.query(MediaFiles).filter(MediaFiles.status==1,MediaFiles.media_url==media_url).first()

            if existUrl:
                return {"status":0,"msg":"This url already used"}

            addCsmSettings = MediaFiles(media_url = media_url,
            title = title,
            description = description,
            meta_title = meta_title,
            brand_name = brand_name,
            media_page = media_page,
            media_position = media_position,
            media_type = media_type,
            start_date = start_date,
            end_date = end_date,
            img_alter = img_alter,
            top_url = top_url,
            bottom_url = bottom_url,
            right_url = right_url,
            left_url = left_url,
            media_orientation = media_orientation,
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

            if top_image:

                uploadedFile = top_image.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(top_image,fName)
                addCsmSettings.top_image = returnFilePath

                db.commit()

            if bottom_image:

                uploadedFile = bottom_image.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(bottom_image,fName)
                addCsmSettings.bottom_image = returnFilePath

                db.commit()
            if right_image:

                uploadedFile = right_image.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(right_image,fName)
                addCsmSettings.right_image = returnFilePath

                db.commit()
            if left_image:

                uploadedFile = left_image.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(left_image,fName)
                addCsmSettings.left_image = returnFilePath

                db.commit()
                

            return {"status":1,"msg":"Successfully Media files added"}

        else:
            return {'status':0,"msg":"You are not authenticated to update media files."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_media_files")
async def updateMediaFiles(db:Session = Depends(deps.get_db),
                     media_files_id:int=Form(...),
                     media_url:str=Form(...),
                     title:str=Form(None),
                     brand_name:str=Form(None),

                     start_date:date=Form(None),
                     end_date:date=Form(None),
                     description:str=Form(None),
                     meta_title:str=Form(None),
                     img_alter:str=Form(None),
                     meta_description:str=Form(None),
                     media_position:int=Form(None,description="1->Top,2-Bottom,3-right,4-Left"),
                       media_page:int=Form(None,description="1->Home,2-Category"),
                     top_image:Optional[UploadFile] = File(None),
                     bottom_image:Optional[UploadFile] = File(None),
                     right_image:Optional[UploadFile] = File(None),
                     left_image:Optional[UploadFile] = File(None),
                        top_url:Optional[UploadFile] = File(None),
                     bottom_url:Optional[UploadFile] = File(None),
                     right_url:Optional[UploadFile] = File(None),
                     left_url:Optional[UploadFile] = File(None),

                    #  content_type:str=Form(None),
                     meta_keywords:str=Form(None),
                     media_file:Optional[UploadFile] = File(None),
                     media_type:int=Form(None,description="1->img,2-shorts,3->Video"),

                     media_orientation:int=Form(None,description="1->Portrait,2-Landscape"),
                    #  seo_url:str=Form(None),
                     token:str=Form(...)
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,7]:

            getMediaFiles = db.query(MediaFiles).filter(MediaFiles.id==media_files_id).first()

            if not getMediaFiles:
                return{"status":0,"msg":"Not Found"}
            existUrl =db.query(MediaFiles).filter(MediaFiles.status==1,MediaFiles.id!=media_files_id,
                                                  MediaFiles.media_url==media_url).first()

            if existUrl:
                return {"status":0,"msg":"This url already used"}
            
            getMediaFiles.media_url = media_url
            getMediaFiles.start_date = start_date
            getMediaFiles.end_date = end_date
            getMediaFiles.brand_name = brand_name
            getMediaFiles.media_page = media_page
            getMediaFiles.media_position = media_position
            getMediaFiles.title = title
            getMediaFiles.media_type = media_type
            getMediaFiles.img_alter = img_alter
            getMediaFiles.media_orientation=media_orientation
            getMediaFiles.top_url = top_url
            getMediaFiles.bottom_url = bottom_url
            getMediaFiles.right_url = right_url
            getMediaFiles.left_url = left_url
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

            if top_image:

                uploadedFile = top_image.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(top_image,fName)
                getMediaFiles.top_image = returnFilePath

                db.commit()

            if bottom_image:

                uploadedFile = bottom_image.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(bottom_image,fName)
                getMediaFiles.bottom_image = returnFilePath

                db.commit()
            if right_image:

                uploadedFile = right_image.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(right_image,fName)
                getMediaFiles.right_image = returnFilePath

                db.commit()
            if left_image:

                uploadedFile = left_image.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(left_image,fName)
                getMediaFiles.left_image = returnFilePath

                db.commit()


            return {"status":1,"msg":"Successfully Media files Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Media files."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/list_media_files")
async def listMediaFiles(db:Session =Depends(deps.get_db),
                       token:str = Form(...),

                       content_type:int=Form(None,description="1->Advertisement,2->Banners,3-youtube,4-shorts"),
                        media_type:int=Form(None,description="1->img,2-shorts,3->Video"),
                        media_page:int=Form(None,description="1->Home,2-Category"),
                       title:str=Form(None),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllAds = db.query(MediaFiles).filter(MediaFiles.status ==1)

            if content_type:
                getAllAds = getAllAds.filter(MediaFiles.content_type==content_type)


            if media_type:
                getAllAds = getAllAds.filter(MediaFiles.media_type==media_type)

            if media_page:
                getAllAds = getAllAds.filter(MediaFiles.media_page==media_page)
            if title:
                getAllAds =  getAllAds.filter(MediaFiles.title.like("%"+title+"%"))

            totalCount = getAllAds.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllAds = getAllAds.limit(limit).offset(offset).all()
            medPositionName =["-","TOP","BOTTOM","RIGHT","LEFT"]
            medOrientationName =["-","Portrait","Landscape"]

            dataList=[]
            if getAllAds:
                for row in getAllAds:
                    dataList.append({
                "media_files_id":row.id,
                "start_date":row.start_date,
                "end_date":row.end_date,
                "media_position_name":medPositionName[row.media_position] if row.media_position else None,
                "top_url":row.top_url,
                "brand_name":row.brand_name,
                "bottom_url":row.bottom_url,
                "left_url":row.left_url,
                "right_url":row.right_url,
                "media_url":row.media_url,
                "media_page":row.media_page,
                "media_position":row.media_position,
                "title":row.title,
                "description":row.description,
                "meta_title":row.meta_title,
                "media_orientation":row.media_orientation,
                "media_orientation_name":medOrientationName[row.media_orientation] if row.media_orientation else None,
                "meta_description":row.meta_description,
                # "seo_url":row.seo_url,
                "img_alter":row.img_alter,
                "media_file":f"{settings.BASE_DOMAIN}{row.img_path}" if row.img_path else "",
                "top_image":f"{settings.BASE_DOMAIN}{row.top_image}" if row.top_image else "",
                "right_image":f"{settings.BASE_DOMAIN}{row.right_image}" if row.right_image else "",
                "left_image":f"{settings.BASE_DOMAIN}{row.left_image}" if row.left_image else "",
                "bottom_image":f"{settings.BASE_DOMAIN}{row.bottom_image}" if row.bottom_image else "",
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
            return {'status':0,"msg":"You are not authenticated to view media_ iles."}
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
        
        medPositionName =["-","TOP","BOTTOM","RIGHT","LEFT"]
        medOrientationName =["-","Portrait","Landscape"]


        data={
            "media_files_id":getData.id,
            "media_position":getData.media_position,
            "start_date":getData.start_date,
            "end_date":getData.end_date,
            "media_position_name":medPositionName[getData.media_position] if getData.media_position else None,

            "media_url":getData.media_url,
            "brand_name":getData.brand_name,
            "top_url":getData.top_url,
            "bottom_url":getData.bottom_url,
            "left_url":getData.left_url,
            "right_url":getData.right_url,
            "media_page":getData.media_page,
            "title":getData.title,
            "media_file":f"{settings.BASE_DOMAIN}{getData.img_path}" if getData.img_path else "",
            "media_orientation_name":medOrientationName[getData.media_orientation] if getData.media_orientation else None,
            "top_image":f"{settings.BASE_DOMAIN}{getData.top_image}" if getData.top_image else "",
            "right_image":f"{settings.BASE_DOMAIN}{getData.right_image}" if getData.right_image else "",
            "left_image":f"{settings.BASE_DOMAIN}{getData.left_image}" if getData.left_image else "",
            "bottom_image":f"{settings.BASE_DOMAIN}{getData.bottom_image}" if getData.bottom_image else "",
            "description":getData.description,
            "img_alter":getData.img_alter,
            "media_orientation":getData.media_orientation,

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