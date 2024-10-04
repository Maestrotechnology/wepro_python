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


@router.post("/list_website_forms")
async def list_website_forms(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       email:str=Form(None),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllWebsiteForms = db.query(WebsiteForms).filter(WebsiteForms.status ==1,WebsiteForms.form_type==3)

            # if series_type:
            #     getAllWebsiteForms = getAllWebsiteForms.filter(WebsiteForms.series_type==series_type)
            if email:
                getAllWebsiteForms =  getAllWebsiteForms.filter(WebsiteForms.email.like("%"+email+"%"))

            totalCount = getAllWebsiteForms.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllWebsiteForms = getAllWebsiteForms.limit(limit).offset(offset).all()



            dataList=[]
            if getAllWebsiteForms:
                for row in getAllWebsiteForms:
                    dataList.append({
                "form_id":row.id,
                "email":row.email,
                "created_at":row.created_at,                  
                      }  )
            
            data=({"page":page,"size":size,
                   "total_page":totalPages,
                   "total_count":totalCount,
                   "items":dataList})
        
            return ({"status":1,"msg":"Success","data":data})
        else:
            return {'status':0,"msg":"You are not authenticated to view ProStories."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})

@router.post("/send_newsletter_email")
async def sendNewsletterEmail(db:Session =Depends(deps.get_db), 
                              token:str = Form(...),
                              form_ids:str = Form(None),
                              is_all:int=Form(None,description="1-send email for everyone")
                      ):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        getAllWebsiteForms = db.query(WebsiteForms).filter(WebsiteForms.status ==1,WebsiteForms.form_type==3)

        if form_ids:
            form_ids = form_ids.split(',')

            getAllWebsiteForms = getAllWebsiteForms.filter(WebsiteForms.id.in_(form_ids))


        getAllWebsiteForms =getAllWebsiteForms.all()

        if not getAllWebsiteForms:
            return {"status":0,"msg":"Not found."}
        
        email = []

        for row in getAllWebsiteForms:
            email.append(row.email)
        
        sendNotifyEmail = await send_mail_req_approval(db=db,email_type=7,article_id=None,user_id=None,
                        receiver_email=email,subject="NewsLetter",journalistName="Subscriber",
                        message="hai",
                    )

        return {"status":1,"msg":"Successfully Newsletter sent."}
                
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/create_cms_settings")
async def createCmsSettings(db:Session = Depends(deps.get_db),
                     google_play:str=Form(None),
                     app_store:str=Form(None),
                     facebook:str=Form(None),
                     instagram:str=Form(None),
                     twitter:str=Form(None),
                     youtube:str=Form(None),
                     wepro_text:str=Form(None),
                     about:str=Form(None),
                     our_teams:str=Form(None),
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
            our_teams = our_teams,
            wepro_text = wepro_text,
            instagram = instagram,
            about = about,
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
                       wepro_text:str=Form(None),
                     about:str=Form(None),
                     our_teams:str=Form(None),
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
            getCms.our_teams = our_teams
            getCms.wepro_text = wepro_text
            getCms.about = about
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
            "our_teams":getCmsSetting.our_teams,
            "facebook":getCmsSetting.facebook,
            "wepro_text":getCmsSetting.wepro_text,
            "about":getCmsSetting.about,
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
    
