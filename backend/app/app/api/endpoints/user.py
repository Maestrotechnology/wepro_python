
from fastapi import APIRouter, Depends, Form,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash
from datetime import datetime,date
from app.utils import *
from sqlalchemy import or_
from typing import Optional


router = APIRouter()


@router.post("/sign_up")
async def signUp(db:Session = Depends(deps.get_db),
                 name:str = Form(...),
                    #  user_name:str=Form(...),
                     phone:str=Form(...),
                     address:str=Form(...),
                     pincode:str=Form(...),
                     dob:date=Form(...),
                     email:str=Form(...),
                     whatsapp_no:str=Form(None),
                     account_number:str=Form(None),
                     bank:str=Form(None),
                     pan_number:str=Form(None),
                     aadhaar_number:str=Form(None),
                     past_designation:str=Form(None),
                     educational_qualification:str=Form(None),
                     previous_experience:str=Form(None),
                     experience_in_relevent_field:str=Form(None),
                     area_of_interest:str=Form(None),
                     ifsc_code:str=Form(None),
                     branch:str=Form(None),
                     state_id:int=Form(None),
                     alternative_no:str=Form(None),
                     resume_file:Optional[UploadFile] = File(None),
                     img_path:Optional[UploadFile] = File(None),

                    #  alt_img:str=Form(None),
                     city_id:int=Form(None),
                     user_type:int=Form(None,description="2->Admin,3->Hr,4->Chief Editor,5->Sub Editor,6-Technical Lead,7->Digital Marketing strategist,8-journalist,9-SEO-Google Strategist,10-Marketing,11-Web designer,12-Graphic Designer")
                     ):
    
   
    getUser = db.query(User).filter(User.status == 1)
        
    if deps.contains_emoji(name):
        return {"status":0,"msg":"Emojis are not allowed to use."}
    # if user_name:
    #     if deps.contains_emoji(user_name):
    #         return {"status":0,"msg":"Emojis are not allowed to use."}
    #     checkUserName = getUser.filter(or_(User.user_name == user_name,User.email==user_name,User.phone==user_name) ).first()
    #     if checkUserName:
    #         return {"status": 0,"msg": "user_name already exists. "}
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
        past_designation = past_designation,
        pan_number = pan_number,
        aadhaar_number = aadhaar_number,
        educational_qualification = educational_qualification,
        area_of_interest = area_of_interest,
        previous_experience = previous_experience,
        experience_in_relevent_field=experience_in_relevent_field,
        whatsapp_no=whatsapp_no,
        email = email,
        phone = phone,
        alternative_no = alternative_no,
        account_number = account_number,
        bank = bank,
        ifsc_code = ifsc_code,
        branch = branch,
        pincode = pincode,
        request_user=1,
        dob = dob,
        address = address,
        state_id = state_id,
        city_id = city_id,
        is_request =1,
        is_active = 1,
        requested_at = datetime.now(settings.tz_IN),
        # created_at = datetime.now(settings.tz_IN),
        # updated_at = datetime.now(settings.tz_IN),
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
        
    subject = "Sign-Up Request Received"
    comment = "Thank you for requesting to sign up! We have received your request, and our team will review it shortly. You will hear from us soon with the next steps."

    mailForSignupUpdate = await send_mail_req_approval(
    db,5,None,createUsers.id,subject,name,email,comment
    )
    return {"status":1,"msg":"Your account creation request has been successfully submitted."}


@router.post("/create_user")
async def createUser(db:Session = Depends(deps.get_db),
                     token:str = Form(...),name:str = Form(...),
                     user_name:str=Form(...),
                     phone:str=Form(...),
                     address:str=Form(...),
                     pincode:str=Form(...),
                     dob:date=Form(...),
                     joining_date:date=Form(None),
                     email:str=Form(...),
                     whatsapp_no:str=Form(None),
                     account_number:str=Form(None),
                     bank:str=Form(None),
                      pan_number:str=Form(None),
                     aadhaar_number:str=Form(None),
                     educational_qualification:str=Form(None),
                     previous_experience:str=Form(None),
                     experience_in_relevent_field:str=Form(None),
                     past_designation:str=Form(None),
                     area_of_interest:str=Form(None),
                     ifsc_code:str=Form(None),
                     branch:str=Form(None),
                     state_id:int=Form(None),
                     alternative_no:str=Form(None),
                     resume_file:Optional[UploadFile] = File(None),
                     img_path:Optional[UploadFile] = File(None),
                    #  alt_img:str=Form(None),
                     city_id:int=Form(None),
                     password:str=Form(...),
                     user_type:int=Form(None,description="2->Admin,3->Hr,4->Chief Editor,5->Sub Editor,6-Technical Lead,7->Digital Marketing strategist,8-journalist,9-SEO-Google Strategist,10-Marketing,11-Web designer,12-Graphic Designer")
                     ):
    
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3,6]:
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
                past_designation = past_designation,
                email = email,
                joining_date = joining_date,
                phone = phone,
                alternative_no = alternative_no,
                account_number = account_number,
                bank = bank,
                ifsc_code = ifsc_code,
                branch = branch,
                pincode = pincode,
                pan_number = pan_number,
                aadhaar_number = aadhaar_number,
                educational_qualification = educational_qualification,
                area_of_interest = area_of_interest,
                previous_experience = previous_experience,
                experience_in_relevent_field=experience_in_relevent_field,
                dob = dob,
                address = address,
                state_id = state_id,
                city_id = city_id,
                is_request =2,
                approved_by =user.id,
                password =  get_password_hash(password),
                is_active = 1,
                created_at = datetime.now(settings.tz_IN),
                updated_at = datetime.now(settings.tz_IN),
                created_by = user.id,
                status =1)
            
            db.add(createUsers)
            db.commit()

            message = (
                    f"Congratulations! Your account has been successfully created."
                    f"You can now proceed with accessing the platform and utilizing the available resources. "
                    f"If you have any questions or need further assistance, please don't hesitate to reach out.<br>"
                    "<div>"
                    "<p style='margin: 0;'>Login Credentials:</p>"
                    f"<p style='margin: 0;'>User Name: {user_name}</p>"
                    f"<p style='margin: 0;'>Password: {password}</p>"
                    "</div>")

            subject = f"Account Creation"
            sendNotifyEmail = await send_mail_req_approval(db=db,email_type=1,article_id=None,user_id=createUsers.id,
                receiver_email=createUsers.email,subject=subject,journalistName=createUsers.name,
                message=message,
            )

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
                     password:str=Form(None),
                     dob:date=Form(...),
                     email:str=Form(...),
                     whatsapp_no:str=Form(None),
                     img_path:Optional[UploadFile] = File(None),
                       pan_number:str=Form(None),
                     aadhaar_number:str=Form(None),
                     past_designation:str=Form(None),
                     educational_qualification:str=Form(None),
                     previous_experience:str=Form(None),
                     experience_in_relevent_field:str=Form(None),
                     area_of_interest:str=Form(None),

                     account_number:str=Form(None),
                     bank:str=Form(None),
                     ifsc_code:str=Form(None),
                     state_id:int=Form(None),
                     city_id:int=Form(None),
                     branch:str=Form(None),
                     resume_file:Optional[UploadFile] = File(None),
                     comment:str=Form(None),
                     approval_status:int=Form(None,description="2-Accpted,3-Interview Process,-1 ->rejected"),
                          
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
     
            # if user_id and user.user_type not in [1,2,3,6]:
            #     return {"status":0,"msg":"You're not allowed to update the user."}
            # elif not user_id:
            #     userId = user.id
            # else:
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
                if password:
                    checkUserId.password =  get_password_hash(password)
                checkUserId.ifsc_code = ifsc_code
                checkUserId.branch = branch
                checkUserId.pincode = pincode
                checkUserId.dob = dob
                checkUserId.past_designation = past_designation

                checkUserId.pan_number = pan_number,
                checkUserId.aadhaar_number = aadhaar_number,
                checkUserId.educational_qualification = educational_qualification,
                checkUserId.area_of_interest = area_of_interest,
                checkUserId.previous_experience = previous_experience,
                checkUserId.experience_in_relevent_field=experience_in_relevent_field,
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

            if approval_status ==2 :
                login_url = "https://wepro.digital/wepro_admin" 
                
                message = (
                    f"Congratulations! Your request for account creation has been successfully approved. "
                    f"You can now proceed with accessing the platform and utilizing the available resources. "
                    f"If you have any questions or need further assistance, please don't hesitate to reach out.<br>"
                    "<div>"
                    "<p style='margin: 0;'>Login Credentials:</p>"
                    f"<p style='margin: 0;'>User Name: {user_name}</p>"
                    f"<p style='margin: 0;'>Password: {password}</p>"
                    "</div>"
                    f"<p>You can login to your account <a href='{login_url}'>here</a>.</p>"
                    )

                if comment:
                    message = (f"{comment}"
                               f"    User Name: {user_name}\n"
                    f"    Password: {password}\n"
                    f"<p>You can login to your account <a href='{login_url}'>here</a>.</p>"
                    )
 
            if approval_status ==3 and not comment:

                message = (
                    "Your application is currently under review as part of the interview process. "
                    "We will keep you updated on the progress and notify you once the review is complete. "
                    "Thank you for your patience, and please feel free to contact us if you have any questions."
                )

            if approval_status ==-1 and not comment:
   
                message = (
                    "We regret to inform you that your request for account creation has been rejected. "
                    "We appreciate your interest and effort. If you have any questions or need feedback on your application, "
                    "please contact us for more details."
                )

            if approval_status:

                approvalSts = ["-","-","Accepted","Interview Process","Rejected"]
                subject = f"User Account {approvalSts[approval_status]}"
                sendNotifyEmail = await send_mail_req_approval(db=db,email_type=1,article_id=None,user_id=checkUserId.id,
                    receiver_email=checkUserId.email,subject=subject,journalistName=checkUserId.name,
                    message=message,
                )

            return {"status":1,"msg":"User successfully updated."}
          
        else:
            return {"status":0,"msg":"You are not authenticated to modify any users."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/list_users")
async def listUser(db:Session =Depends(deps.get_db),
                   token:str=Form(...),page:int=1,
                   size:int=10,phone:str=Form(None),
                   user_type:int=Form(None,description="1->SuperAdmin,2->Admin,3->Hr,4->Chief Editor,5->Sub Editor,6-Technical Lead,7->Digital Marketing strategist,8-journalist,9-Member,10-SEO-Google Strategist,11-Marketing,12-Web designer,13-Graphic Designer"),
                   email:str=Form(None),state_id:int=Form(None),city_id:int=Form(None),
                   name:str=Form(None),
                   is_requested:int=Form(None),
                   application_status:int=Form(None,description="1->Request,2-Accepted,3-interview process,-1 ->rejected")
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user:
            
            getAllUser = db.query(User).filter(User.status==1)

            if user_type:
                getAllUser = getAllUser.filter(User.user_type == user_type)


            if is_requested:
                getAllUser = getAllUser.filter(User.is_request != 2)


            if application_status:
                getAllUser = getAllUser.filter(User.is_request == application_status)

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

            if user.user_type in [1,2,3,6]:
                getJournalReq=db.query(User).filter(User.status==1,User.is_request==1).count()
                journalistReq = getJournalReq

            getAllUser = getAllUser.order_by(User.id.desc())
            
            userCount = getAllUser.count()
            totalPages,offset,limit = get_pagination(userCount,page,size)
            getAllUser = getAllUser.limit(limit).offset(offset).all()
            
            userTypeData = ["-","-","Admin","Hr","Chief Editor","Sub Editor","Technical Lead","Digital Marketing strategist","Journalist","SEO-Google Strategist","Marketing","Web designer","Graphic Designer"]
            dataList = []
            if getAllUser:
                for userData in getAllUser:
                    dataList.append(
                        {
                            "user_id":userData.id,
                            "user_name":userData.user_name,
                            "name":userData.name,
                            "alternative_no":userData.alternative_no,
                            "address":userData.address,
                            "phone":userData.phone,
                            "whatsapp_no":userData.whatsapp_no,
                            "email":userData.email,
                            "resume_file":f'{settings.BASE_DOMAIN}{userData.resume_path}',
                            "joining_date":userData.joining_date,
                            "dob":userData.dob,
                            "past_designation":userData.past_designation,
                            "city_id":userData.city_id,
                            "is_request":userData.is_request,
                            "city_name":userData.cities.name if userData.city_id else None,
                            "state_id":userData.state_id,
                            "state_name":userData.states.name if userData.state_id else None,
                            "pincode":userData.pincode,
                            "account_number":userData.account_number,
                            "experience_in_relevent_field":userData.experience_in_relevent_field,
                            "bank":userData.bank,
                            "ifsc_code":userData.ifsc_code,
                            "branch":userData.branch,
                            "user_status":userData.is_active,
                            "user_type":userData.user_type,
                            "user_type_name": userTypeData[userData.user_type] if userData.user_type else None,
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
            
            getAllNotify = db.query(ArticleHistory).filter(ArticleHistory.status==1)

            
            getAllNotify = getAllNotify.filter(ArticleHistory.journalist_id==user.id,
                                                ArticleHistory.journalist_notify==1).count()
            notifyCount = getAllNotify

            data ={
            "user_id":getUser.id,
                "user_name":getUser.user_name,
                "name":getUser.name,
                "address":getUser.address,
                "phone":getUser.phone,
                "whatsapp_no":getUser.whatsapp_no,
                "dob":getUser.dob,
                "past_designation":getUser.past_designation,
                "alternative_no":getUser.alternative_no,

                "email":getUser.email,
                "city_id":getUser.city_id,
                "city_name":getUser.cities.name if getUser.city_id else None,
                "state_id":getUser.state_id,
                "state_name":getUser.states.name if getUser.state_id else None,
                "pincode":getUser.pincode,
                "account_number":getUser.account_number,
                "experience_in_relevent_field":getUser.experience_in_relevent_field,
                "bank":getUser.bank,
                "ifsc_code":getUser.ifsc_code,
                "branch":getUser.branch,
                "joining_date":getUser.joining_date,
                "user_status":getUser.is_active,
                "user_type":getUser.user_type,
                "resume_file":f'{settings.BASE_DOMAIN}{getUser.resume_path}' if getUser.resume_path else None,
                "img_path":f'{settings.BASE_DOMAIN}{getUser.img_path}',
                "notification_count":notifyCount,

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
        if user.user_type in [1,2,3,4,5,6] :
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
        if user.user_type in [1,2,3,6]:
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
                           
                             approval_status:int=Form(...,description="2-Accpted,3-Interview Process,-1 ->rejected"),
                            user_name:str=Form(None),
                            password:str=Form(None),
                             comment:str=Form(None)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getUser = db.query(User).filter(User.id == user_id,
                                            User.status == 1).first()
            getUser.is_request=approval_status
            db.commit()

            message =comment

            if approval_status ==2 :
                getUser.approved_by=user.id

                # getUser.user_name = user_name
                getUser.approved_at = datetime.now(settings.tz_IN)


                # if password:
                #     getUser.password =  get_password_hash(password)

                db.commit()

                userTypeData = ["-","-","Admin","Hr","Chief Editor","Sub Editor","Technical Lead","Digital Marketing strategist","Journalist","SEO-Google Strategist","Marketing","Web designer","Graphic Designer"]

                addNotification = Notification(
                user_id = getUser.id,
                comment =f'{user.user_name} approved the {userTypeData[getUser.user_type]} account creation for {getUser.user_name}. ' ,
                title = f'{user.user_name}({userTypeData[user.user_type]}) - Account Approved',
                status=1,
                admin_notify=1,
                notification_type=4,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id

                )
                db.add(addNotification)
                db.commit()
                
            #     message = (
            #         f"Congratulations! Your request for account creation has been successfully approved. "
            #         f"You can now proceed with accessing the platform and utilizing the available resources. "
            #         f"If you have any questions or need further assistance, please don't hesitate to reach out.<br>"
            #         "<div>"
            #         "<p style='margin: 0;'>Login Credentials:</p>"
            #         "<p style='margin: 0;'>User Name: {user_name}</p>"
            #         "<p style='margin: 0;'>Password: {password}</p>"
            #         "</div>")

            #     if comment:
            #         message = (f"{comment}"
            #                    f"    User Name: {user_name}\n"
            #         f"    Password: {password}\n")
 
            # if approval_status ==3 and not comment:

            #     message = (
            #         "Your application is currently under review as part of the interview process. "
            #         "We will keep you updated on the progress and notify you once the review is complete. "
            #         "Thank you for your patience, and please feel free to contact us if you have any questions."
            #     )

            if approval_status ==-1 and not comment:
                getUser.rejected_by=user.id
                getUser.status=-1
                getUser.rejected_at = datetime.now(settings.tz_IN)
                db.commit()
            if approval_status ==-1 and not comment:
            
                message = (
                    "We regret to inform you that your request for account creation has been rejected. "
                    "We appreciate your interest and effort. If you have any questions or need feedback on your application, "
                    "please contact us for more details."
                )


                approvalSts = ["-","-","Accepted","Interview Process","Rejected"]
                subject = f"User Account {approvalSts[approval_status]}"
                sendNotifyEmail = await send_mail_req_approval(db=db,email_type=1,article_id=None,user_id=getUser.id,
                    receiver_email=getUser.email,subject=subject,journalistName=getUser.name,
                    message=message,
                )

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
                   email_type:int=Form(None),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user:
            
            getAllEmailHistory = db.query(EmailHistory).filter(EmailHistory.to_email == to_email,EmailHistory.status==1)

            if subject:
                getAllEmailHistory = getAllEmailHistory.filter(EmailHistory.subject.like("%"+subject+"%") )
            if article_id:
                getAllEmailHistory = getAllEmailHistory.filter(EmailHistory.article_id == article_id)

            if email_type:
                getAllEmailHistory = getAllEmailHistory.filter(EmailHistory.email_type == email_type)
            
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
