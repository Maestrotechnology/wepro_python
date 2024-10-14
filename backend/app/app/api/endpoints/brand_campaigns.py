from fastapi import APIRouter, Depends, Form,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from datetime import datetime
from app.utils import *
from datetime import datetime
from typing import Optional



router = APIRouter()

@router.post("/create_brand_campaigns")
async def createBrandCampaigns(db:Session = Depends(deps.get_db),
                     title:str=Form(None),
                     description:str=Form(None),
                     sort_order:int=Form(None),
                     brand_url:str=Form(None),
                     img_alter:str=Form(None),
                     token:str=Form(...),
                     media_type:int=Form(None,description="1->image,2-gif"),
                     media_file:Optional[UploadFile] = File(None),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,7,6]:

            addBrandCam = BrandCampaigns(
            title = title,
            description = description,
            media_type = media_type,
            sort_order = sort_order,
            brand_url = brand_url,
            img_alter = img_alter,
            status=1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addBrandCam)
            db.commit()

            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                addBrandCam.img_path = returnFilePath

                db.commit()

            return {"status":1,"msg":"Successfully Brand Campaign Added"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Brand Campaign."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_brand_campaigns")
async def updateBrandCampaigns(db:Session = Depends(deps.get_db),
                     brand_campaigns_id:int=Form(...),
                    title:str=Form(None),
                     description:str=Form(None),
                     sort_order:int=Form(None),
                     brand_url:str=Form(None),
                     img_alter:str=Form(None),
                     token:str=Form(...),
                     media_type:int=Form(None,description="1->image,-1->gif"),
                     media_file:Optional[UploadFile] = File(None),
                     
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,7,6]:

            getBrandCampaigns = db.query(BrandCampaigns).filter(BrandCampaigns.id==brand_campaigns_id).first()

            if not getBrandCampaigns:
                return{"status":0,"msg":"Not Found"}
            
            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                getBrandCampaigns.img_path = returnFilePath

                db.commit()
            
            getBrandCampaigns.title = title
            getBrandCampaigns.img_alter = img_alter
            getBrandCampaigns.description = description
            getBrandCampaigns.sort_order = sort_order
            getBrandCampaigns.brand_url = brand_url
            getBrandCampaigns.media_type = media_type
            getBrandCampaigns.updated_at = datetime.now(settings.tz_IN)
            getBrandCampaigns.updated_by = user.id

            db.commit()

            return {"status":1,"msg":"Successfully Brand Campaign Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Brand Campaign."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/list_brand_campaigns")
async def listBrandCampaigns(db:Session =Depends(deps.get_db),
                       token:str = Form(None),
                       media_type:int=Form(None),
                       title:str=Form(None),
                       page:int=1,size:int = 10):
        
    if token:
        user=deps.get_user_token(db=db,token=token)
        if user:
            pass

        else:
            return {'status':0,"msg":"You are not authenticated to view Brand Campaign."}
        
    getAllBrandCam = db.query(BrandCampaigns).filter(BrandCampaigns.status ==1)

    if media_type:
        getAllBrandCam = getAllBrandCam.filter(BrandCampaigns.media_type==media_type)
    
    if title:
        getAllBrandCam =  getAllBrandCam.filter(BrandCampaigns.title.like("%"+title+"%"))


    totalCount = getAllBrandCam.count()
    totalPages,offset,limit = get_pagination(totalCount,page,size)
    getAllBrandCam = getAllBrandCam.limit(limit).offset(offset).all()

    dataList=[]
    if getAllBrandCam:
        for row in getAllBrandCam:
            dataList.append({
        "brand_campaigns_id":row.id,
        "title":row.title,
        "description":row.description,
        "media_type":row.media_type,
        "brand_url":row.brand_url,
        "media_file":f"{settings.BASE_DOMAIN}{row.img_path}",
        "sort_order":row.sort_order,
        "img_alter":row.img_alter,
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
    
@router.post("/view_brand_campaigns")
async def viewBrandCampaigns(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   brand_campaigns_id:int=Form(...),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
            
        getBrandCam = db.query(BrandCampaigns).filter(
            BrandCampaigns.status==1,BrandCampaigns.id==brand_campaigns_id).first()
        
        if not getBrandCam:
            return {"status":0,"msg":"No Record Found"}

        data={
            "brand_campaigns_id":getBrandCam.id,
            "title":getBrandCam.title,
            "media_type":getBrandCam.media_type,
            "description":getBrandCam.description,
            "img_alter":getBrandCam.img_alter,
            "sort_order":getBrandCam.sort_order,
            "media_file":f"{settings.BASE_DOMAIN}{getBrandCam.img_path}" if getBrandCam.img_path else None,
            "brand_url":getBrandCam.brand_url,
            "created_at":getBrandCam.created_at,                  
            "updated_at":getBrandCam.updated_at,                  
            "created_by":getBrandCam.createdBy.user_name if getBrandCam.created_by else None,                  
            "updated_by":getBrandCam.updatedBy.user_name if getBrandCam.updated_by else None,                  
            }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/delete_brand_campaigns")
async def deleteBrandCampaigns(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     brand_campaigns_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,6] :
            getBrandCampaigns = db.query(BrandCampaigns).filter(BrandCampaigns.id == brand_campaigns_id,
                                            BrandCampaigns.status == 1)
            
            getBrandCampaigns = getBrandCampaigns.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"BrandCampaigns successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete Brand Campaign"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}

