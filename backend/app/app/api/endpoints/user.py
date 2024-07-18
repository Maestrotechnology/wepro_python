
from fastapi import APIRouter, Depends, Form,requests,UploadFile,File
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime,date
from app.utils import *
from sqlalchemy import or_
from app.core import security
from typing import List, Optional,Dict


router = APIRouter()




@router.post("/create_user")
async def createUser(db:Session = Depends(deps.get_db),
                     token:str = Form(...),name:str = Form(...),
                     user_name:str=Form(...),
                     phone:str=Form(...),
                     address:str=Form(...),
                     pincode:str=Form(...),
                     dob:date=Form(...),
                     email:str=Form(...),
                     whatsapp_no:str=Form(None),
                     account_number:str=Form(None),
                     bank:str=Form(None),
                     ifsc_code:str=Form(None),
                     branch:str=Form(None),
                     state_id:int=Form(None),
                     alternative_no:str=Form(None),
                     resume_file:Optional[UploadFile] = File(None),
                     img_path:Optional[UploadFile] = File(None),
                    #  alt_img:str=Form(None),
                     city_id:int=Form(None),
                     password:str=Form(...),
                     user_type:int=Form(None,description="2->Admin,3->Hr,4->Chief Editor,5->Sub Editor,6->Digital Marketing strategist,7-journalist,8-Member")
                     ):
    
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3]:
            getUser = db.query(User).filter(User.status == 1)
            password = password.strip()
             
            if deps.contains_emoji(name):
                return {"status":0,"msg":"Emojis are not allowed to use."}
            if user_name:
                if deps.contains_emoji(user_name):
                    return {"status":0,"msg":"Emojis are not allowed to use."}
                checkUserName = getUser.filter(or_(User.user_name == user_name,User.email==user_name,User.phone==user_name) ).first()
                if checkUserName:
                    return {"status": 0,"msg": "user_name already exists. "}
            if deps.contains_emoji(email):
                return {"status":0,"msg":"Emojis are not allowed to use in email"}
            checkEmail = getUser.filter(User.email == email ).first()
            if checkEmail:
                return {"status":0,"msg":"Email already exists."}
            
            checkMobileNumber = getUser.filter(User.phone == phone).first()
            if checkMobileNumber:
                return {"status":0,"msg":"Mobile already in use."}
            if state_id:
                checkState = db.query(States).filter(States.id == state_id,States.status==1).first()
                if not checkState:
                    return {"status" : 0 , "msg" : "Invalid state."}
            if  city_id:
                checkCity = db.query(Cities).filter(Cities.id == city_id).first()
                if not checkCity:
                    return {"status":0,"msg":"Invalid city."}
            
            createUsers = User(
                user_type = user_type,
                name = name,
                whatsapp_no=whatsapp_no,
                user_name = user_name,
                email = email,
                phone = phone,
                alternative_no = alternative_no,
                account_number = account_number,
                bank = bank,
                ifsc_code = ifsc_code,
                branch = branch,
                pincode = pincode,
                dob = dob,
                address = address,
                state_id = state_id,
                city_id = city_id,
                is_request =2 if user_type==7 else None,
                # approved_by =user.id if user_type==7 else None,
                password =  get_password_hash(password),
                is_active = 1,
                created_at = datetime.now(settings.tz_IN),
                updated_at = datetime.now(settings.tz_IN),
                created_by = user.id,
                status =1)
            
            db.add(createUsers)
            db.commit()

            if resume_file:

                uploadedFile = resume_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(resume_file,fName)
                createUsers.resume_path = returnFilePath

                db.commit()

            if img_path:

                uploadedFile = img_path.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(img_path,fName)
                createUsers.img_path = returnFilePath

                db.commit()

            return {"status":1,"msg":"User created successfully."}
        else:
            return {'status':0,"msg":"You are not authenticated to create a user."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_user")
async def updateUser (db:Session=Depends(deps.get_db),
                     token:str = Form(...),name:str = Form(...),
                     user_id:int=Form(None),
                     user_name:str=Form(...),
                     phone:str=Form(...),
                     alternative_no:str=Form(None),
                     address:str=Form(...),
                     pincode:str=Form(...),
                     dob:date=Form(...),
                     email:str=Form(...),
                     whatsapp_no:str=Form(None),
                     img_path:Optional[UploadFile] = File(None),

                     account_number:str=Form(None),
                     bank:str=Form(None),
                     ifsc_code:str=Form(None),
                     state_id:int=Form(None),
                     city_id:int=Form(None),
                     branch:str=Form(None),
                     resume_file:Optional[UploadFile] = File(None),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
     
            if user_id and user.user_type not in [1,2,3]:
                return {"status":0,"msg":"You're not allowed to update the user."}
            elif not user_id:
                userId = user.id
            else:
                userId =user_id

            if deps.contains_emoji(user_name):
                return {"status":0,"msg":"Emojis are not allowed to use."}
            if deps.contains_emoji(email):
                return {"status":0,"msg":"Emojis are not allowed to use in email."}
            if deps.contains_emoji(name):
                return {"status":0,"msg":"Emojis are not allowed to use in email."}
         
            
            getUser = db.query(User).filter(User.status ==1)
            checkUserId = getUser.filter(User.id == userId).first()
            ExceptUser = getUser.filter(User.id != userId)
            
            if checkUserId:
                if user_name:
                    checkUserName = ExceptUser.filter(or_(User.user_name == user_name,User.email==user_name,User.phone==user_name) ).first()
                    if checkUserName:
                        return {"status": 0,"msg": "user_name already exists. "}
                    
                checkEmail = ExceptUser.filter(User.email == email ).first()
                if checkEmail:
                    return {"status":0,"msg":"Email already exists."}
                
                checkMobileNumber = ExceptUser.filter(or_(User.phone == phone,
                                                          User.alternative_no == phone)).first()

                if checkMobileNumber:
                    return {"status":0,"msg":"Mobile already in use."}
                
                if state_id:
                    checkState = db.query(States).filter(States.id == state_id,States.status==1).first()
                    if not checkState:
                        return {"status" : 0 , "msg" : "Invalid state."}
                    
                if  city_id:
                    checkCity = db.query(Cities).filter(Cities.id == city_id).first()
                    if not checkCity:
                        return {"status":0,"msg":"Invalid city."}
                    
                
                checkUserId.name = name
                checkUserId.whatsapp_no=whatsapp_no
                checkUserId.user_name = user_name
                checkUserId.email = email
                checkUserId.phone = phone
                checkUserId.alternative_no = alternative_no
                checkUserId.account_number = account_number
                checkUserId.bank = bank
                checkUserId.ifsc_code = ifsc_code
                checkUserId.branch = branch
                checkUserId.pincode = pincode
                checkUserId.dob = dob
                checkUserId.address = address
                checkUserId.state_id = state_id
                checkUserId.city_id = city_id
                checkUserId.updated_by = user.id 
                checkUserId.updated_at = datetime.now(settings.tz_IN)
                
                db.commit()

                if resume_file:

                    uploadedFile = resume_file.filename
                    fName,*etn = uploadedFile.split(".")
                    filePath,returnFilePath = file_storage(resume_file,fName)
                    checkUserId.resume_path = returnFilePath

                
            if img_path:

                uploadedFile = img_path.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(img_path,fName)
                checkUserId.img_path = returnFilePath

                db.commit()

            return {"status":1,"msg":"User successfully updated."}
          
        else:
            return {"status":0,"msg":"You are not authenticated to modify any users."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/list_users")
async def listUser(db:Session =Depends(deps.get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,phone:str=Form(None),
                   user_type:int=Form(...,description="2->Admin,3->Hr,4->Chief Editor,5->Sub Editor,6->Digital Marketing strategist,7-journalist,8-Member"),
                   email:str=Form(None),state_id:int=Form(None),city_id:int=Form(None),
                   name:str=Form(None),
                   application_status:int=Form(None,description="0->Request,1-interview process,-1 ->rejected")
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user:
            
            getAllUser = db.query(User).filter(User.user_type == user_type,User.status==1)

            if user_type==7 and (application_status!=0 and not application_status):
                getAllUser = getAllUser.filter(User.is_request == 2)

            if phone:
                getAllUser = getAllUser.filter(User.phone== phone )
            if email:
                getAllUser = getAllUser.filter(User.email == email)
            if state_id:
                getAllUser = getAllUser.filter(User.state_id == state_id)
            if city_id:
                getAllUser = getAllUser.filter(User.city_id == city_id)
            if name:
                getAllUser = getAllUser.filter(User.name.like("%"+name+"%"))

            journalistReq = 0

            if application_status==0 or application_status:
                getAllUser = getAllUser.filter(User.is_request == application_status)
      

            if user.user_type in [1,2,3]:
                getJournalReq=db.query(User).filter(User.user_type == 7,User.status==1,User.is_request==0).count()
                journalistReq = getJournalReq

            getAllUser = getAllUser.order_by(User.name.asc())
            
            userCount = getAllUser.count()
            totalPages,offset,limit = get_pagination(userCount,page,size)
            getAllUser = getAllUser.limit(limit).offset(offset).all()
            
            userTypeData = ["-","-","Admin","Hr","Chief Editor","Sub Editor","Digital Marketing strategist","Journalist","Member"]
            dataList = []
            if getAllUser:
                for userData in getAllUser:
                    dataList.append(
                        {
                            "user_id":userData.id,
                            "user_name":userData.user_name,
                            "name":userData.name,
                            "address":userData.address,
                            "phone":userData.phone,
                            "whatsapp_no":userData.whatsapp_no,
                            "email":userData.email,
                            "dob":userData.dob,
                            "city_id":userData.city_id,
                            "city_name":userData.cities.name if userData.city_id else None,
                            "state_id":userData.state_id,
                            "state_name":userData.states.name if userData.state_id else None,
                            "pincode":userData.pincode,
                            "account_number":userData.account_number,
                            "bank":userData.bank,
                            "ifsc_code":userData.ifsc_code,
                            "branch":userData.branch,
                            "user_status":userData.is_active,
                            "user_type":userData.user_type,
                            "user_type_name": userTypeData[userData.user_type],
                        }
                    )
            data=({"journalist_req_count":journalistReq,
                   "page":page,"size":size,
                    "total_page":totalPages,
                    "total_count":userCount,
                    "items":dataList})
            
            return ({"status":1,"msg":"Success.","data":data})
        else:
            return {"status":0,"msg":"You are not authenticated to see the user details."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    
@router.post("/view_user")
async def viewUser(db:Session=Depends(deps.get_db),
                   token:str=Form(...),
                   user_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getUser = db.query(User).filter(User.id == user_id,
                                            User.status == 1).first()
            
            if not getUser:
                return {"status":0,"msg":"No user Found"}
            data ={
            "user_id":getUser.id,
                "user_name":getUser.user_name,
                "name":getUser.name,
                "address":getUser.address,
                "phone":getUser.phone,
                "whatsapp_no":getUser.whatsapp_no,
                "dob":getUser.dob,
                "email":getUser.email,
                "city_id":getUser.city_id,
                "city_name":getUser.cities.name if getUser.city_id else None,
                "state_id":getUser.state_id,
                "state_name":getUser.states.name if getUser.state_id else None,
                "pincode":getUser.pincode,
                "account_number":getUser.account_number,
                "bank":getUser.bank,
                "ifsc_code":getUser.ifsc_code,
                "branch":getUser.branch,
                "user_status":getUser.is_active,
                "user_type":getUser.user_type,
                "resume_path":f'{settings.BASE_DOMAIN}{getUser.resume_path}',
                "img_path":f'{settings.BASE_DOMAIN}{getUser.img_path}'

            }
            return {"status":1,"msg":"Success.","data":data}
        else:
            return {'status':0,"msg":"You are not authenticated to view any user."}
    return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/delete_user")
async def deleteUser(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     userId:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2] :
            getUser = db.query(User).filter(User.id == userId,
                                            User.status == 1)
            
            getUser = getUser.update({"status":-1,"is_active":-1})
            db.commit()
            return {"status":1,"msg":"User successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete any user"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}

@router.post("/active_inactive_user")
async def activeInactiveUser(db:Session=Depends(deps.get_db),
                             token:str=Form(...),user_id:int=Form(...),
                             activeStatus:int=Form(...,description="1->active,2->inactive")):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2]:
            getUser = db.query(User).filter(User.id == user_id,
                                            User.status == 1)
            getUser = getUser.update({"is_active":activeStatus})
            db.commit()
            message ="Success."
            if activeStatus ==1:
                message ="User successfully activated."
            else:
                message ="User successfully deactivated."

            return {"status":1,"msg":message}
        else:
            return {'status':0,"msg":"You are not authenticated to change status of any user"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
    
@router.post("/change_journalist_request")
async def changeJournalistRequest(db:Session=Depends(deps.get_db),
                             token:str=Form(...),user_id:int=Form(...),
                             approval_status:int=Form(...,description="1->Interview Process,2-Approved,-1->Rejected")):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3]:
            getUser = db.query(User).filter(User.id == user_id,
                                            User.status == 1).first()
            getUser.is_request=approval_status
            getUser.approved_by=user.id
            db.commit()
            message ="Success."
            if approval_status ==2:
                message ="Journalist account creation request successfully approved."

            if approval_status ==1:
                message ="You're now in the interview process. Once it's complete, you'll be approved."

            if approval_status ==-1:
                message ="Journalist account creation request successfully Rejected."

            approvalSts = ["-","Interview Process","Approved","Rejected"]
            subject = f"Jouranl Account {approvalSts[approval_status]}"
            sendNotifyEmail = await send_mail_req_approval(db=db,
                receiver_email=getUser.email,subject=subject,
                message=message,
            )

            # if sendNotifyEmail["status"] != 1:
            #     return {"status": 1, "msg": "Failed to send email"}

            return {"status":1,"msg":"success"}
        else:
            return {'status':0,"msg":"You are not authenticated to change status of any user"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
    


@router.post("/list_email_history")
async def listEmailHistory(db:Session =Depends(deps.get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,
                   to_email:str=Form(None),
                   subject:str=Form(None),
                   article_id:int=Form(None),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user:
            
            getAllEmailHistory = db.query(EmailHistory).filter(EmailHistory.to_email == to_email,EmailHistory.status==1)

            if subject:
                getAllEmailHistory = getAllEmailHistory.filter(EmailHistory.subject.like("%"+subject+"%") )
            if article_id:
                getAllEmailHistory = getAllEmailHistory.filter(EmailHistory.article_id == article_id)
            
            getAllEmailHistory = getAllEmailHistory.order_by(EmailHistory.name.asc())
            
            userCount = getAllEmailHistory.count()
            totalPages,offset,limit = get_pagination(userCount,page,size)
            getAllEmailHistory = getAllEmailHistory.limit(limit).offset(offset).all()
            
            dataList = []
            if getAllEmailHistory:
                for history in getAllEmailHistory:
                    dataList.append(
                        {
                            "email_history_id":history.id,
                            "from_email":history.from_email,
                            "to_email":history.to_email,
                            "subject":history.subject,
                            "message":history.message,
                            "article_id":history.article_id,
                            "created_at":history.created_at
                        }
                    )
            data=({"page":page,"size":size,
                    "total_page":totalPages,
                    "total_count":userCount,
                    "items":dataList})
            
            return ({"status":1,"msg":"Success.","data":data})
        else:
            return {"status":0,"msg":"You are not authenticated to see the user details."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
