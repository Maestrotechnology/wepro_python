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


@router.post("/create_career")
async def createCareers(db:Session = Depends(deps.get_db),
                     title:str=Form(...),
                     description:str=Form(...),
                     token:str=Form(...),
                     salary:float=Form(...),
                     requirements:str=Form(...),
                     employement_type:int=Form(...,description='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary'),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user:

            existTitle = db.query(Careers).filter(Careers.title==title,Careers.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}

            addCareers = Careers(
            title = title,
            salary = salary,
            description = description,
            requirements = requirements,
            employement_type = employement_type,
            status=1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addCareers)
            db.commit()

            return {"status":1,"msg":"Successfully Careers Added"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Careers."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_career")
async def updateCareers(db:Session = Depends(deps.get_db),
                     career_id:int=Form(...),
                    title:str=Form(...),
                     description:str=Form(...),
                     token:str=Form(...),
                     salary:float=Form(...),
                     requirements:str=Form(...),
                     employement_type:int=Form(...,description='1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary'),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user:

            existTitle = db.query(Careers).filter(Careers.id!=career_id,
                                                   Careers.title==title,Careers.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}


            getCareers = db.query(Careers).filter(Careers.id==career_id).first()

            if not getCareers:
                return{"status":0,"msg":"Not Found"}

            getCareers.title = title
            getCareers.requirements = requirements
            getCareers.employement_type = employement_type
            getCareers.description = description
            getCareers.salary = salary
            getCareers.updated_at = datetime.now(settings.tz_IN)
            getCareers.updated_by = user.id

            db.commit()

            return {"status":1,"msg":"Successfully Careers Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update Careers."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/list_career")
async def listCareers(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       title:str=Form(None),
                       employement_type :int=Form(None,description="1-full-time, 2-part-time, 3-contract, 4-internship, 5-temporary"),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllCareers = db.query(Careers).filter(Careers.status ==1)


            if title:
                getAllCareers =  getAllCareers.filter(Careers.title.like("%"+title+"%"))

            if employement_type:
                getAllCareers = getAllCareers.filter(Careers.employement_type==employement_type)


            totalCount = getAllCareers.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllCareers = getAllCareers.limit(limit).offset(offset).all()

            dataList=[]
            if getAllCareers:
                for row in getAllCareers:
                    dataList.append({
                "career_id":row.id,
                "title":row.title,
                "salary":row.salary,
                "description":row.description,
                "requirements":row.requirements,
                "employement_type":row.employement_type,
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
            return {'status':0,"msg":"You are not authenticated to view Careers."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
    
@router.post("/view_career")
async def viewCareers(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   career_id:int=Form(...),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
            
        getCareers = db.query(Careers).filter(
            Careers.status==1,Careers.id==career_id).first()
        
        if not getCareers:
            return {"status":0,"msg":"No Record Found"}

        data={
                "career_id":getCareers.id,
                "title":getCareers.title,
                "salary":getCareers.salary,
                "description":getCareers.description,
                "requirements":getCareers.requirements,
                "employement_type":getCareers.employement_type,
                "created_at":getCareers.created_at,                  
                "updated_at":getCareers.updated_at,                  
                "created_by":getCareers.createdBy.user_name if getCareers.created_by else None,                  
                "updated_by":getCareers.updatedBy.user_name if getCareers.updated_by else None,                  
                      }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/delete_career")
async def deleteCareers(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     career_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getCareers = db.query(Careers).filter(Careers.id == career_id,
                                            Careers.status == 1)
            
            getCareers = getCareers.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"Careers successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete career"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
    
