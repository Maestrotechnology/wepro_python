from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from datetime import datetime
from app.utils import *
from datetime import datetime
from typing import List, Optional,Dict



router = APIRouter()


@router.post("/create_cms_settings")
async def createCmsSettings(db:Session = Depends(deps.get_db),
                     google_play:str=Form(None),
                     app_store:str=Form(None),
                     facebook:str=Form(None),
                     instagram:str=Form(None),
                     twitter:str=Form(None),
                     youtube:str=Form(None),
                     threads:str=Form(None),
                     linkedin:str=Form(None),
                     token:str=Form(...)
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2]:

            addCsmSettings = CmsSettings(google_play = google_play,
            app_store = app_store,
            facebook = facebook,
            instagram = instagram,
            twitter = twitter,
            youtube = youtube,
            linkedin = linkedin,
            threads = threads,
            status=1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addCsmSettings)
            db.commit()

            return {"status":1,"msg":"Successfully Cms Settings Created"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Cms Settings."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_cms_settings")
async def updateCmsSettings(db:Session = Depends(deps.get_db),
                     cms_settings_id:int=Form(...),
                     google_play:str=Form(None),
                     app_store:str=Form(None),
                     facebook:str=Form(None),
                     instagram:str=Form(None),
                     twitter:str=Form(None),
                     youtube:str=Form(None),
                     threads:str=Form(None),
                     linkedin:str=Form(None),
                     token:str=Form(...)
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2]:

            getCms = db.query(CmsSettings).filter(CmsSettings.id==cms_settings_id).first()

            if not getCms:
                return{"status":0,"msg":"Not Found"}
            
            getCms.google_play = google_play
            getCms.app_store = app_store
            getCms.facebook = facebook
            getCms.twitter = twitter
            getCms.instagram = instagram
            getCms.youtube = youtube
            getCms.linkedin = linkedin
            getCms.threads = threads
            getCms.updated_at = datetime.now(settings.tz_IN)
            getCms.updated_by = user.id

            db.commit()

            return {"status":1,"msg":"Successfully Cms Settings Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Cms Settings."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/view_csms_settings")
async def viewCmsSettings(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   cms_settings_id:int=Form(...),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
            
        getCmsSetting = db.query(CmsSettings).filter(
            CmsSettings.status==1,CmsSettings.id==cms_settings_id).first()
        
        if not getCmsSetting:
            return {"status":0,"msg":"No Record Found"}

        data={
            "cms_settings_id":getCmsSetting.id,
            "google_play":getCmsSetting.google_play,
            "app_store":getCmsSetting.app_store,
            "facebook":getCmsSetting.facebook,
            "instagram":getCmsSetting.instagram,
            "twitter":getCmsSetting.twitter,
            "youtube":getCmsSetting.youtube,
            "linkedin":getCmsSetting.linkedin,
            "threads":getCmsSetting.threads,
            "created_at":getCmsSetting.created_at,                  
            "updated_at":getCmsSetting.updated_at,                  
            "created_by":getCmsSetting.createdBy.user_name if getCmsSetting.created_by else None,                  
            "updated_by":getCmsSetting.updatedBy.user_name if getCmsSetting.updated_by else None,                  
            }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    
