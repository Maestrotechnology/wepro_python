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


@router.post("/create_category")
async def createCategory(db:Session = Depends(deps.get_db),
                     title:str=Form(...),
                     description:str=Form(...),
                     img_alter:str=Form(...),
                     seo_url:str=Form(None),
                     sort_order:int=Form(...),
                     token:str=Form(...),
                     media_file:Optional[UploadFile] = File(None),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3]:

            existTitle = db.query(Category).filter(Category.title==title,Category.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}

            addCategory = Category(
            title = title,
            img_alter = img_alter,
            seo_url = seo_url,
            description = description,
            sort_order = sort_order,
            status=1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addCategory)
            db.commit()

            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                addCategory.img_path = returnFilePath

                db.commit()

            return {"status":1,"msg":"Successfully Category Added"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Category."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_category")
async def updateCategory(db:Session = Depends(deps.get_db),
                     category_id:int=Form(...),
                    title:str=Form(...),
                     description:str=Form(...),
                     img_alter:str=Form(...),
                     seo_url:str=Form(None),
                     sort_order:int=Form(...),
                     token:str=Form(...),
                     media_file:Optional[UploadFile] = File(None),
                     
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2]:

            existTitle = db.query(Category).filter(Category.id!=category_id,
                                                   Category.title==title,Category.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}


            getCategory = db.query(Category).filter(Category.id==category_id).first()

            if not getCategory:
                return{"status":0,"msg":"Not Found"}
            
            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                getCategory.img_path = returnFilePath

                db.commit()
            
            getCategory.title = title
            getCategory.seo_url = seo_url
            getCategory.img_alter = img_alter
            getCategory.description = description
            getCategory.sort_order = sort_order
            getCategory.updated_at = datetime.now(settings.tz_IN)
            getCategory.updated_by = user.id

            db.commit()

            return {"status":1,"msg":"Successfully Category Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Category."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/list_category")
async def listCategory(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       title:str=Form(None),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllCategory = db.query(Category).filter(Category.status ==1)


            if title:
                getAllCategory =  getAllCategory.filter(Category.title.like("%"+title+"%"))


            totalCount = getAllCategory.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllCategory = getAllCategory.limit(limit).offset(offset).all()

            dataList=[]
            if getAllCategory:
                for row in getAllCategory:
                    dataList.append({
                "category_id":row.id,
                "title":row.title,
                "seo_url":row.seo_url,
                "description":row.description,
                "img_path":f"{settings.BASE_DOMAIN}{row.img_path}",
                "img_alter":row.img_alter,
                "sort_order":row.sort_order,
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
            return {'status':0,"msg":"You are not authenticated to view Category."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
    
@router.post("/view_category")
async def viewCategory(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   category_id:int=Form(...),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
            
        getCategory = db.query(Category).filter(
            Category.status==1,Category.id==category_id).first()
        
        if not getCategory:
            return {"status":0,"msg":"No Record Found"}

        data={
            "category_id":getCategory.id,
            "title":getCategory.title,
            "seo_url":getCategory.seo_url,
            "description":getCategory.description,
            "img_alter":getCategory.img_alter,
            "sort_order":getCategory.sort_order,
            "img_path":f"{settings.BASE_DOMAIN}{getCategory.img_path}",
            "created_at":getCategory.created_at,                  
            "updated_at":getCategory.updated_at,                  
            "created_by":getCategory.createdBy.user_name if getCategory.created_by else None,                  
            "updated_by":getCategory.updatedBy.user_name if getCategory.updated_by else None,                  
            }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/delete_category")
async def deleteCategory(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     category_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3] :
            getCategory = db.query(Category).filter(Category.id == category_id,
                                            Category.status == 1)
            
            getCategory = getCategory.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"Category successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete category"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
    





@router.post("/create_sub_category")
async def createSubCategory(db:Session = Depends(deps.get_db),
                     title:str=Form(None),
                     description:str=Form(None),
                     img_alter:str=Form(None),
                     sort_order:int=Form(None),
                     category_id:int=Form(...),
                     token:str=Form(...),
                     media_file:Optional[UploadFile] = File(None),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3]:

            existTitle = db.query(Category).filter(Category.id!=category_id,
                                                   Category.title==title,Category.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}

            addSubCategory = SubCategory(
            title = title,
            img_alter = img_alter,
            sort_order = sort_order,
            description = description,
            category_id = category_id,
            status=1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addSubCategory)
            db.commit()

            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                addSubCategory.img_path = returnFilePath

                db.commit()

            return {"status":1,"msg":"Successfully SubCategory Added"}

        else:
            return {'status':0,"msg":"You are not authenticated to update SubCategory."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_sub_category")
async def updateSubCategory(db:Session = Depends(deps.get_db),
                     sub_category_id:int=Form(...),
                    img_alter:str=Form(None),
                    title:str=Form(None),
                     sort_order:int=Form(None),

                     description:str=Form(None),
                     token:str=Form(...),
                     media_file:Optional[UploadFile] = File(None),
                     
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2]:

            existTitle = db.query(SubCategory).filter(SubCategory.id!=sub_category_id,
                                                   SubCategory.title==title,SubCategory.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}

            getSubCategory = db.query(SubCategory).filter(SubCategory.id==sub_category_id).first()

            if not getSubCategory:
                return{"status":0,"msg":"Not Found"}
            
            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                getSubCategory.img_path = returnFilePath

                db.commit()
            
            getSubCategory.img_alter = img_alter
            getSubCategory.sort_order = sort_order
            getSubCategory.title = title
            getSubCategory.description = description
            getSubCategory.updated_at = datetime.now(settings.tz_IN)
            getSubCategory.updated_by = user.id

            db.commit()

            return {"status":1,"msg":"Successfully SubCategory Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update SubCategory."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/list_sub_category")
async def listSubCategory(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       title:str=Form(None),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllSubCategory = db.query(SubCategory).filter(SubCategory.status ==1)


            if title:
                getAllSubCategory =  getAllSubCategory.filter(SubCategory.title.like("%"+title+"%"))


            totalCount = getAllSubCategory.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllSubCategory = getAllSubCategory.limit(limit).offset(offset).all()

            dataList=[]
            if getAllSubCategory:
                for row in getAllSubCategory:
                    dataList.append({
                "sub_category_id":row.id,
                "title":row.title,
                "img_alter":row.img_alter,
                "description":row.description,
                "category_id":row.category_id,
                "category_title": row.category.title if row.category_id else None,
                "img_path":f"{settings.BASE_DOMAIN}{row.img_path}",
                "sort_order":row.sort_order,
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
            return {'status':0,"msg":"You are not authenticated to view SubCategory."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
    
@router.post("/view_sub_category")
async def viewSubCategory(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   sub_category_id:int=Form(...),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
            
        getSubCategory = db.query(SubCategory).filter(
            SubCategory.status==1,SubCategory.id==sub_category_id).first()
        
        if not getSubCategory:
            return {"status":0,"msg":"No Record Found"}

        data={
            "sub_category_id":getSubCategory.id,
            "category_title": getSubCategory.category.title if getSubCategory.category_id else None,

            "title":getSubCategory.title,
            "img_alter":getSubCategory.img_alter,
            "description":getSubCategory.description,
            "sort_order":getSubCategory.sort_order,
            "img_path":f"{settings.BASE_DOMAIN}{getSubCategory.img_path}",
            "created_at":getSubCategory.created_at,                  
            "updated_at":getSubCategory.updated_at,                  
            "created_by":getSubCategory.createdBy.user_name if getSubCategory.created_by else None,                  
            "updated_by":getSubCategory.updatedBy.user_name if getSubCategory.updated_by else None,                  
            }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/delete_sub_category")
async def deleteSubCategory(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     sub_category_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3] :
            getSubCategory = db.query(SubCategory).filter(SubCategory.id == sub_category_id,
                                            SubCategory.status == 1)
            
            getSubCategory = getSubCategory.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"SubCategory successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete sub category"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}