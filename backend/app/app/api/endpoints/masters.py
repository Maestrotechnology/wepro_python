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
        if user.user_type in [1,2,3,6]:

            existTitle = db.query(Category).filter(Category.title==title,Category.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}
            
            existSeoUrl = db.query(Category).filter(Category.seo_url==seo_url,Category.status==1).first()

            if existSeoUrl:
                return {"status":0,"msg":"This SeoUrl already used."}

            addCategory = Category(
            title = title,
            img_alter = img_alter,
            seo_url = seo_url,
            description = description,
            sort_order = sort_order,
            status=1,
            is_active=1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addCategory)
            db.commit()

            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                addCategory.img_path = returnFilePath


                if etn[0].lower() == 'png':
                    addCategory.img_type = 1  # Assign 1 for PNG
                elif etn[0].lower() == 'jpg':
                    addCategory.img_type = 2  # Assign 2 for JPG or JPEG
                elif etn[0].lower() == 'jpeg':
                    addCategory.img_type = 3
                else:
                    # Handle other file types if necessary
                    addCategory.img_path = returnFilePath
                    addCategory.img_type = 0  

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
        if user.user_type in [1,2,6]:

            existTitle = db.query(Category).filter(Category.id!=category_id,
                                                   Category.title==title,Category.status==1).first()

            if existTitle:
                return {"status":0,"msg":"This Title already used."}
            
            existSeoUrl = db.query(Category).filter(Category.seo_url==seo_url,Category.id!=category_id,Category.status==1).first()

            if existSeoUrl:
                return {"status":0,"msg":"This SeoUrl already used."}

            getCategory = db.query(Category).filter(Category.id==category_id).first()

            if not getCategory:
                return{"status":0,"msg":"Not Found"}
            
            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                getCategory.img_path = returnFilePath


                if etn[0].lower() == 'png':
                    getCategory.img_type = 1  # Assign 1 for PNG
                elif etn[0].lower() == 'jpg':
                    getCategory.img_type = 2  # Assign 2 for JPG or JPEG
                elif etn[0].lower() == 'jpeg':
                    getCategory.img_type = 3 # Assign 2 for JPG or JPEG

                else:
                    # Handle other file types if necessary
                    getCategory.img_type = 0  


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
                "is_active":row.is_active,
                "description":row.description,
                "media_file":f"{settings.BASE_DOMAIN}{row.img_path}",
                "img_alter":row.img_alter,
                "img_type":row.img_type,
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
            "img_type":getCategory.img_type,
            "description":getCategory.description,
            "is_active":getCategory.is_active,
            "img_alter":getCategory.img_alter,
            "sort_order":getCategory.sort_order,
            "media_file":f"{settings.BASE_DOMAIN}{getCategory.img_path}" if getCategory.img_path else None,
            "created_at":getCategory.created_at,                  
            "updated_at":getCategory.updated_at,                  
            "created_by":getCategory.createdBy.user_name if getCategory.created_by else None,                  
            "updated_by":getCategory.updatedBy.user_name if getCategory.updated_by else None,                  
            }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/active_inactive_category")
async def activeInactiveCategory(db:Session=Depends(deps.get_db),
                             token:str=Form(...),category_id:int=Form(...),
                             activeStatus:int=Form(...,description="1->active,2->inactive")):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getCategory = db.query(Category).filter(Category.id == category_id,
                                            Category.status == 1)
            getCategory = getCategory.update({"is_active":activeStatus})
            db.commit()
            message ="Success."
            if activeStatus ==1:
                message ="Category successfully activated."
            else:
                message ="Category successfully deactivated."

            return {"status":1,"msg":message}
        else:
            return {'status':0,"msg":"You are not authenticated to change status of any category"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}

@router.post("/delete_category")
async def deleteCategory(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     category_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3,6] :

            checkSub = db.query(SubCategory).filter(SubCategory.status==1,SubCategory.category_id==category_id).first()

            if checkSub:
                 return {"status": 0, "msg": "Category cannot be deleted because it contains active subcategories. Please delete the related subcategories first."}
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
        if user.user_type in [1,2,3,6]:

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
                     category_id:int=Form(...),
                    img_alter:str=Form(None),
                    title:str=Form(None),
                     sort_order:int=Form(None),

                     description:str=Form(None),
                     token:str=Form(...),
                     media_file:Optional[UploadFile] = File(None),
                     
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,6]:

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
            getSubCategory.category_id = category_id
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
                "media_file":f"{settings.BASE_DOMAIN}{row.img_path}",
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
            "media_file":f"{settings.BASE_DOMAIN}{getSubCategory.img_path}",
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
        if user.user_type in [1,2,3,6] :
            getSubCategory = db.query(SubCategory).filter(SubCategory.id == sub_category_id,
                                            SubCategory.status == 1)
            
            getSubCategory = getSubCategory.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"SubCategory successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete sub category"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/active_inactive_sub_category")
async def activeInactiveSubCategory(db:Session=Depends(deps.get_db),
                             token:str=Form(...),sub_category_id:int=Form(...),
                             activeStatus:int=Form(...,description="1->active,2->inactive")):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getSubCategory = db.query(SubCategory).filter(SubCategory.id == sub_category_id,
                                            SubCategory.status == 1)
            getSubCategory = getSubCategory.update({"is_active":activeStatus})
            db.commit()
            message ="Success."
            if activeStatus ==1:
                message ="SubCategory successfully activated."
            else:
                message ="SubCategory successfully deactivated."

            return {"status":1,"msg":message}
        else:
            return {'status':0,"msg":"You are not authenticated to change status of any sub category"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}

#--Article topic


@router.post("/add_topic")
async def addTopic(db:Session = Depends(deps.get_db),
                     topic:str=Form(...),
                     description:str=Form(None),
                     category_id:int=Form(...),
                     sub_category_id:int=Form(...),
                     token:str=Form(...),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user:

            existTopic = db.query(ArticleTopic).filter(ArticleTopic.id!=category_id,
                                                   ArticleTopic.topic==topic,ArticleTopic.status==1).first()

            if existTopic:
                return {"status":0,"msg":"This Topic already Created."}

            addArticleTopic = ArticleTopic(
            topic = topic,
            description = description,
            category_id = category_id,
            sub_category_id = sub_category_id,
            status=1,
            is_approved=2 if user.user_type==5 else 1,
            created_at = datetime.now(settings.tz_IN),
            created_by = user.id)

            db.add(addArticleTopic)
            db.commit()

            if user.user_type==4:
                addArticleTopic.approved_by=user.id
                addArticleTopic.is_approved=1
                db.commit()

                addNotification = Notification(
                topic_id = addArticleTopic.id,
                comment =f"The topic is {topic}" ,
                title=f"{user.name}(Chief Editor)-added new Topic",
                status=1,
                notification_type=4,
                created_at =datetime.now(settings.tz_IN),
                admin_notify=1,
                created_by = user.id

                )
                db.add(addNotification)
                db.commit()

            if user.user_type==5:
                addHistory = ArticleHistory(
                # comment = f" {approvedStatus[approved_status]}" if not comment else comment,
                comment =f"Sub Editor requested new {topic}"  ,
                title=f"{user.user_name}(Sub Editor)- Editor Topic Requested",
                topic_id=addArticleTopic.id,
                sub_editor_id = user.id ,
                chief_editor_notify =1,
                status=1,
                history_type=3,
                is_editor = 1,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id
            )
                db.add(addHistory)
                db.commit()


            return {"status":1,"msg":"Successfully ArticleTopic Added"}

        else:
            return {'status':0,"msg":"You are not authenticated to update ArticleTopic."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/update_article_topic")
async def updateArticleTopic(db:Session = Depends(deps.get_db),
                     article_topic_id:int=Form(...),
                    topic:str=Form(None),
                     description:str=Form(None),
                     category_id:int=Form(...),
                     sub_category_id:int=Form(...),

                     token:str=Form(...),
                     
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user:
            existTopic = db.query(ArticleTopic).filter(ArticleTopic.id!=article_topic_id,
                                                   ArticleTopic.topic==topic,ArticleTopic.status==1).first()

            if existTopic:
                return {"status":0,"msg":"This topic already used."}

            getArticleTopic = db.query(ArticleTopic).filter(ArticleTopic.id==article_topic_id).first()

            if not getArticleTopic:
                return{"status":0,"msg":"Not Found"}
            

            getArticleTopic.topic = topic
            getArticleTopic.category_id = category_id
            getArticleTopic.sub_category_id = sub_category_id

            getArticleTopic.description = description
            getArticleTopic.updated_at = datetime.now(settings.tz_IN)
            getArticleTopic.updated_by = user.id

            db.commit()

            return {"status":1,"msg":"Successfully ArticleTopic Updated"}

        else:
            return {'status':0,"msg":"You are not authenticated to update ArticleTopic."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/list_article_topic")
async def listArticleTopic(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       topic:str=Form(None),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllArticleTopic = db.query(ArticleTopic).filter(ArticleTopic.status ==1,ArticleTopic.is_choosed==None)


            if topic:
                getAllArticleTopic =  getAllArticleTopic.filter(ArticleTopic.topic.like("%"+topic+"%"))
            
            if user.user_type==8:
                getAllArticleTopic = getAllArticleTopic.filter(ArticleTopic.is_approved==1)

            totalCount = getAllArticleTopic.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllArticleTopic = getAllArticleTopic.order_by(ArticleTopic.id.desc()).limit(limit).offset(offset).all()

            dataList=[]
            name=["-","approved","comment","-"]

            if getAllArticleTopic:
                for row in getAllArticleTopic:
                    dataList.append({
                    "article_topic_id":row.id,
                "topic":row.topic,
                "description":row.description,
                "is_approved":row.is_approved,
                "comment":row.comment,
                "is_approved_name":name[row.is_approved] if row.is_approved else None,
                "category_id":row.category_id,
                "sub_category_id":row.sub_category_id,
                "category_title": row.category.title if row.category_id else None,
                "sub_category_title": row.sub_category.title if row.sub_category_id else None,
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
            return {'status':0,"msg":"You are not authenticated to view ArticleTopic."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
    
@router.post("/view_article_topic")
async def viewArticleTopic(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   article_topic_id:int=Form(...),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
            
        getArticleTopic = db.query(ArticleTopic).filter(
            ArticleTopic.status==1,ArticleTopic.id==article_topic_id).first()
        
        if not getArticleTopic:
            return {"status":0,"msg":"No Record Found"}

        data={
            "article_topic_id":getArticleTopic.id,
            "category_title": getArticleTopic.category.title if getArticleTopic.category_id else None,
            "topic":getArticleTopic.topic,
            "description":getArticleTopic.description,
            "created_at":getArticleTopic.created_at,                  
            "updated_at":getArticleTopic.updated_at,                  
            "created_by":getArticleTopic.createdBy.user_name if getArticleTopic.created_by else None,                  
            "updated_by":getArticleTopic.updatedBy.user_name if getArticleTopic.updated_by else None,                  
            }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/delete_article_topic")
async def deleteArticleTopic(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     article_topic_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user :
            getArticleTopic = db.query(ArticleTopic).filter(ArticleTopic.id == article_topic_id,
                                            ArticleTopic.status == 1)
            
            
            getArticleTopic = getArticleTopic.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"ArticleTopic successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete sub category"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}