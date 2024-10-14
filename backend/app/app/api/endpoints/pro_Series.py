from fastapi import APIRouter, Depends, Form,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.schemas import *
from app.api import deps
from app.core.config import settings
from datetime import datetime
from app.utils import *
from datetime import datetime
from typing import Optional,List
from sqlalchemy import or_
import json
from pydantic import BaseModel


router = APIRouter()

@router.post("/create_pro_stories")
async def createProStories(db:Session = Depends(deps.get_db),
                     token:str=Form(...),
                     title:str=Form(...),
                     description:str=Form(...),
                     url:str=Form(None),
                     img_path:Optional[UploadFile] = File(None),
                     upload_files: Optional[List[UploadFile]] = File(None),
                     multi_image_url:str=Form(None),

                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,6]:

            existTitle = db.query(ProStories).filter(ProStories.title==title,ProStories.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}


            addProStories = ProStories(
            title = title,
            url = url,
            description = description,
            status=1,
            series_type=1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addProStories)
            db.commit()

            if img_path:

                uploadedFile = img_path.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(img_path,fName)
                addProStories.img_path = returnFilePath


                db.commit()
            imageData =[]

            if isinstance(multi_image_url, str):
                multi_image_url = multi_image_url.split(',')


            if upload_files:

                for file,eachUrl in zip(upload_files,multi_image_url):
                        uploadedFile = file.filename
                        fName,*etn = uploadedFile.split(".")
                        filePath,returnFilePath = file_storage(file,fName)


                        imageData.append({
                            "url":eachUrl,
                            "img_path" : returnFilePath,
                            "created_at" : datetime.now(settings.tz_IN),
                            "status" : 1,
                            "series_type":2,
                            "parent_id":addProStories.id,
                            "created_by":user.id
                        })
                        # print(returnFilePath)
                    
                try:
                    with db as conn:
                        conn.execute(ProStories.__table__.insert().values(imageData))
                        conn.commit()
                    return {"status":1,"msg":"Successfully ProStories Added"}
                
                except Exception as e:
                    
                    print(f"Error during bulk insert: {str(e)}")
                    return {"status": 0,"msg": "Failed to insert image"}
                
            return {"status":1,"msg":"Successfully ProStories Added"}

        else:
            return {'status':0,"msg":"You are not authenticated to add ProStories."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_pro_stories_files")
async def updateProStories(db:Session = Depends(deps.get_db),
                      token:str=Form(...),
                      pro_stories_id:int=Form(...),
                     title:str=Form(None),
                     description:str=Form(None),
                     url:str=Form(None),
                     img_path:Optional[UploadFile] = File(None),
                    upload_files: Optional[List[UploadFile]] = File(None),
                     multi_image_url:str=Form(None),
                    #   editFiles: str = Form(None)
                     ):
    
    user=deps.get_user_token(db=db,token=token)

    
    if user:
        if user.user_type in [1,2,3,6]:
            getProStories = db.query(ProStories).filter(ProStories.status==1,
                                                        ProStories.id==pro_stories_id).first()
            
            if not getProStories:
                return {"status":0,"msg":"Not Found"}

            if title:

                existTitle = db.query(ProStories).filter(ProStories.id!=getProStories.id,ProStories.title==title,ProStories.status==1).first()

                if existTitle:
                    return {"status":0,"msg":"This Title already used."}


                getProStories.title = title
            if url:
                getProStories.url = url
            if description:
                getProStories.description = description

            db.commit()

            # edit_files_list = json.loads(editFiles)
            # expectDelIds=[]
            
            # # Process each file_id and file_url
            # for file_data in edit_files_list:
            #     file_id = file_data.get("id")
            #     file_url = file_data.get("url")
            #     if file_id and file_url:
            #         getProFiles= db.query(ProStories).filter(ProStories.id==file_id).first()
            #         if getProFiles:
            #             getProFiles.url=file_url
            #             db.commit()
            #             expectDelIds.append(file_id)

            # deletePro = db.query(ProStories).filter(ProStories.status==1,
            #                                         ProStories.parent_id==getProStories.id,
            #                                         ProStories.id.notin_(expectDelIds)).update({"status":-1}, synchronize_session='fetch')
            # db.commit()


            if img_path:

                uploadedFile = img_path.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(img_path,fName)
                getProStories.img_path = returnFilePath


                db.commit()

            imageData = []

            if isinstance(multi_image_url, str):
                multi_image_url = multi_image_url.split(',')


            if upload_files:

                for file,eachUrl in zip(upload_files,multi_image_url):
                        uploadedFile = file.filename
                        fName,*etn = uploadedFile.split(".")
                        filePath,returnFilePath = file_storage(file,fName)


                        imageData.append({
                            "url":eachUrl,
                            "img_path" : returnFilePath,
                            "created_at" : datetime.now(settings.tz_IN),
                            "status" : 1,
                            "series_type":2,
                            "parent_id":getProStories.id,
                            "created_by":user.id
                        })
                        # print(returnFilePath)
                    
                try:
                    with db as conn:
                        conn.execute(ProStories.__table__.insert().values(imageData))
                        conn.commit()
                    return {"status":1,"msg":"Successfully ProStories Added"}
                
                except Exception as e:
                    
                    print(f"Error during bulk insert: {str(e)}")
                    return {"status": 0,"msg": "Failed to insert image"}
          
                
            return {"status":1,"msg":"Successfully ProStories Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update ProStories."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/list_pro_stories")
async def listProStories(db:Session =Depends(deps.get_db),
                       token:str = Form(None),
                       title:str=Form(None),
                    #    series_type:int=Form(...,description='1-Parent, 2-child'),
                       pro_stories_id:int=Form(None),
                       page:int=1,size:int = 10):
    
    if token:
        user=deps.get_user_token(db=db,token=token)
        if user:
            pass
        else:
            return {'status':0,"msg":"You are not authenticated to view ProStories."}
        
    getAllProStories = db.query(ProStories).filter(ProStories.status ==1)

    # if series_type:
    #     getAllProStories = getAllProStories.filter(ProStories.series_type==series_type)
    
    if pro_stories_id:
        getAllProStories = getAllProStories.filter(ProStories.parent_id==pro_stories_id)
            
    else:
        getAllProStories = getAllProStories.filter(ProStories.series_type==1)
            
    if title:
        getAllProStories =  getAllProStories.filter(ProStories.title.like("%"+title+"%"))


    totalCount = getAllProStories.count()
    totalPages,offset,limit = get_pagination(totalCount,page,size)
    if not pro_stories_id:
        getAllProStories = getAllProStories.limit(limit).offset(offset).all()
    else:
        getAllProStories = getAllProStories.all()


    dataList=[]
    if getAllProStories:
        for row in getAllProStories:
            dataList.append({
        "pro_stories_id":row.id,
        "title":row.title,
        "url":row.url,
        "description":row.description,
        "img_path":f"{settings.BASE_DOMAIN}{row.img_path}",
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



@router.post("/delete_pro_stories")
async def deleteProStories(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     pro_stories_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3,6] :
            getProStories = db.query(ProStories).filter(ProStories.id == pro_stories_id,
                                            ProStories.status == 1)
            
            getProStories = getProStories.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"ProStories successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete pro series"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
    