from fastapi import APIRouter, Depends, Form,requests,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_,and_
from app.core import security
from typing import List, Optional,Dict

from sqlalchemy import func

router = APIRouter()


@router.post("/create_article")
async def CreateArticle(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   topic:str=Form(...),
                   content:str=Form(...),
                   meta_title:str=Form(None),
                   meta_description:str=Form(None),
                   meta_keywords:str=Form(None),
                   seo_url:str=Form(None),
                   category_id:int=Form(...),
                   sub_category_id:int=Form(...),
                   city_id:int=Form(...),
                   state_id:int=Form(...),
                   article_files: Optional[List[UploadFile]] = File(None),
                   img_alter:str=Form(None),
                   ):
    
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user.user_type in [1,2]:

            addArticle = Article(
                topic=topic,
                content=content,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                seo_url=seo_url,
                category_id=category_id,
                content_approved=3,
                topic_approved=3,
                sub_category_id=sub_category_id,
                city_id=city_id,
                state_id=state_id,
                status=1,
                created_by = user.id,
                created_at = datetime.now(settings.tz_IN)
            )
            db.add(addArticle)
            db.commit()

            if article_files :
                row = 0
                imageData =[]
                for file in article_files:
                    uploadedFile = file.filename
                    fName,*etn = uploadedFile.split(".")
                    filePath,returnFilePath = file_storage(file,fName)

                    imageData.append({
                        "img_path" : returnFilePath,
                        "img_alter" : img_alter,
                        "created_at" : datetime.now(settings.tz_IN),
                        "status" : 1,
                        "article_id":addArticle.id,
                        "created_by":user.id
                    })
                    row += 1
                
                try:
                    with db as conn:
                        conn.execute(ArticleFiles.__table__.insert().values(imageData))
                        conn.commit()
                except Exception as e:
                    addArticle.status=-1
                    db.commit()
                    print(f"Error during bulk insert: {str(e)}")
                    return ({"status":0,"msg":"Error during article creation"})

        return ({"status":1,"msg":"Successfully New Article Published. "})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    
@router.post("/update_article")
async def updateArticle(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   article_id:int=Form(...),
                   topic:str=Form(...),
                   content:str=Form(...),
                   meta_title:str=Form(None),
                   meta_description:str=Form(None),
                   meta_keywords:str=Form(None),
                   seo_url:str=Form(None),
                   city_id:int=Form(...),
                   state_id:int=Form(...),
                   article_files: Optional[List[UploadFile]] = File(None),
                   img_alter:str=Form(None),
                   ):
    
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user.user_type in [1,2]:

            getArticle = db.query(Article).filter(Article.id==article_id,
                                            Article.status==1).first()

            if not getArticle:
                return {"status":0,"msg":"Article Not Found"}
            
            getArticle.topic=topic
            getArticle.content=content
            getArticle.meta_title=meta_title
            getArticle.meta_description=meta_description
            getArticle.meta_keywords=meta_keywords
            getArticle.seo_url=seo_url
            getArticle.content_approved=2
            getArticle.topic_approved=2
            getArticle.city_id=city_id
            getArticle.state_id=state_id
            getArticle.status=1
            getArticle.updated_by = user.id
            getArticle.updated_at = datetime.now(settings.tz_IN)
            db.commit()

            if article_files :

                delFiles = db.query(ArticleFiles).\
                    filter(ArticleFiles.article_id==getArticle.id).update({"status":-1})
                
                db.commit()

                row = 0
                imageData =[]
                for file in article_files:
                    uploadedFile = file.filename
                    fName,*etn = uploadedFile.split(".")
                    filePath,returnFilePath = file_storage(file,fName)

                    imageData.append({
                        "img_path" : returnFilePath,
                        "img_alter" : img_alter,
                        "created_at" : datetime.now(settings.tz_IN),
                        "status" : 1,
                        "article_id":getArticle.id,
                        "created_by":user.id
                    })
                    row += 1
                
                try:
                    with db as conn:
                        conn.execute(ArticleFiles.__table__.insert().values(imageData))
                        conn.commit()
                except Exception as e:

                    print(f"Error during bulk insert: {str(e)}")
                    # return ({"status":0,"msg":"Error during article Update"})

        return ({"status":1,"msg":"Successfully Article Updated. "})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

 
@router.post("/view_article")
async def viewArticle(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   article_id:int=Form(...),
                   ):
    user = deps.get_user_token(db=db,token=token)

    if user:
            
        getArticle = db.query(Article).filter(
            Article.status==1,Article.id==article_id).first()
        
        if not getArticle:
            return {"status":0,"msg":"No Record Found"}
        
        getAllFiles=db.query(ArticleFiles).filter(ArticleFiles.status==1,
                                        ArticleFiles.article_id==getArticle.id).all()
        
        articleFiles=[]

        for eachFile in getAllFiles:
            articleFiles.append({
                "image_id":eachFile.id,
                "img_path":f'{settings.BASE_DOMAIN}{eachFile.img_path}',
                "img_alter":eachFile.img_alter,
            })
        
        approvedStatus =["New","Sub Edior Approved","Chief Editor Approved","On Hold"]

        data={
            "article_id":getArticle.id,
            "topic":getArticle.topic,
            "content":getArticle.content,
            "submition_date":getArticle.submition_date,
            "meta_title":getArticle.meta_title,
            "meta_description":getArticle.meta_description,
            "meta_keywords":getArticle.meta_keywords,
            "seo_url":getArticle.seo_url,
            "state_id":getArticle.state_id,
            "state_name":getArticle.states.name if getArticle.state_id else None,
            "city_id":getArticle.city_id,
            "is_journalist":getArticle.is_journalist,
            "city_name":getArticle.cities.name if getArticle.city_id else None,
            "topic_approved": approvedStatus[getArticle.topic_approved] if getArticle.topic_approved else None,
            "content_approved": approvedStatus[getArticle.content_approved] if getArticle.content_approved else None,
            "approval_chief_editor":getArticle.chief_editor_id,
            "chief_editor_name":getArticle.chiefEditerUser.user_name if getArticle.chief_editor_id else None, 
            "sub_editor_name":getArticle.subEditerUser.user_name if getArticle.sub_editor_id else None, 
            "approval_sub_editor":getArticle.sub_editor_id,
            "article_images":articleFiles,
            "comment":getArticle.comment,
            "created_at":getArticle.created_at,                  
            "updated_at":getArticle.updated_at,                  
            "journalist_id":getArticle.created_by,                 
            "journalist_name":getArticle.createdBy.user_name if getArticle.created_by else None,              
            "updated_by":getArticle.updatedBy.user_name if getArticle.updated_by else None,                  
            }

        return ({"status":1,"msg":"Success.","data":data})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/list_article")
async def listArticle(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       category_id:int=Form(None),
                       city_id:int=Form(None),
                       state_id:int=Form(None),
                       sub_category_id:int=Form(None),
                       topic_approval_status:int=Form(None,description="0->new,1->SE approved,2-CE Approved,3-On Hold"),
                       contant_approval_status:int=Form(None,description="0->new,1->SE approved,2-CE Approved,3-On Hold"),
                       page:int=1,size:int = 10):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllArticle = db.query(Article).filter(Article.status ==1)

            if state_id:
                getAllArticle = getAllArticle.filter(Article.state_id==state_id)

            if city_id:
                getAllArticle = getAllArticle.filter(Article.city_id==city_id)

            if category_id:
                getAllArticle = getAllArticle.filter(Article.category_id==category_id)

            if sub_category_id:
                getAllArticle = getAllArticle.filter(Article.sub_category_id==sub_category_id)

            if topic_approval_status:
                getAllArticle = getAllArticle.filter(Article.topic_approved==topic_approval_status)

            if contant_approval_status:
                
                getAllArticle = getAllArticle.filter(Article.content_approved==contant_approval_status)

            notifyCount = 0

            getAllNotify = db.query(ArticleHistory).filter(ArticleHistory.status==1)

            if user.user_type ==4:
                getAllNotify = getAllNotify.filter(ArticleHistory.chief_editor_id==user.id,
                                                   ArticleHistory.chief_editor_notify==1).count()
                notifyCount = getAllNotify

            if user.user_type ==5:
                getAllNotify = getAllNotify.filter(ArticleHistory.sub_editor_id==user.id,
                                                   ArticleHistory.sub_editor_notify==1).count()
                notifyCount = getAllNotify

            if user.user_type ==7:
                getAllNotify = getAllNotify.filter(ArticleHistory.journalist_id==user.id,
                                                   ArticleHistory.journalist_notify==1).count()
                notifyCount = getAllNotify

            totalCount = getAllArticle.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllArticle = getAllArticle.limit(limit).offset(offset).all()

            dataList=[]

            stsName = ["new","SE approved","CE Approved","Approved","On Hold"]
            if getAllArticle:
                for row in getAllArticle:
                    dataList.append({
                "article_id":row.id,
                "topic":row.topic,
                "content":row.content,
                "topic_approved":row.topic_approved,
                "topic_approved_name":stsName[row.topic_approved] if row.topic_approved else None ,
                "content_approved":row.content_approved,
                "content_approved_name":stsName[row.content_approved] if row.content_approved else None,
                "created_at":row.created_at,                  
                "updated_at":row.updated_at, 
                "journalist_id":row.created_by,                 
                "journalist_name":row.createdBy.user_name if row.created_by else None,                  
                "updated_by":row.updatedBy.user_name if row.updated_by else None,                  
                      }  )
            
            data=({"notification_count":notifyCount,"page":page,"size":size,
                   "total_page":totalPages,
                   "total_count":totalCount,
                   "items":dataList})
        
            return ({"status":1,"msg":"Success","data":data})
        else:
            return {'status':0,"msg":"You are not authenticated to view Article."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})


    
@router.post("/article_topic_approve")
async def articleTopicApprove(db:Session = Depends(deps.get_db),
                     token:str=Form(...),
                     comment : str=Form(None),
                     article_id:int=Form(...),
                     approved_status:int=Form(...,description="1->SE approved,2-CE Approved,3-On Hold"),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,4,5]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            
            topicApproved = 0
            approvedStatus =["new","SE approved","CE Approved","On Hold"]
            
            journalistEmail = getArticle.createdBy.email if getArticle.created_by else None

            if user.user_type==4:
                getArticle.topic_approved = approved_status
                getArticle.chief_editor_id =user.id

                if approved_status in [2,3]:
                    comment = f"The Article Topic is {approvedStatus[approved_status]}" if not comment else comment

                    subject ="Artcle Update"
                    mailForArticleUpdate = await send_mail_req_approval(
                    db,subject,journalistEmail,comment
                    )

            if user.user_type==5:
                getArticle.topic_approved = approved_status
                getArticle.sub_editor_id =user.id

                if approved_status in [3]:
                    journalistEmail = getArticle.createdBy.email if getArticle.created_by else None
                    comment = f"The Article Topic is {approvedStatus[approved_status]}" if not comment else comment

                    subject ="Artcle Update"
                    mailForArticleUpdate = await send_mail_req_approval(
                    db,subject,comment,journalistEmail
                    )

            if user.user_type in [1,2]:
                getArticle.topic_approved = approved_status

            db.commit()

            if comment:
                getArticle.comment = comment
                db.commit()


            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f"The Article Topic is {approvedStatus[approved_status]}" if not comment else comment,
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 0 if user.user_type==5 else 1,
                chief_editor_notify =(0 if user.user_type==4 else (1
                                       if user.user_type in [1,2,3,5] and approved_status==1 else None)),
                journalist_notify = 1,
                status=1,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id
            )
            db.add(addHistory)
            db.commit()


            return {"status":1,"msg":"Article topic approval updated successfully"}

        else:
            return {'status':0,"msg":"You are not authenticated to update topic approval."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    
    
@router.post("/article_content_approve")
async def articleContentApprove(db:Session = Depends(deps.get_db),
                     token:str=Form(...),
                     comment : str=Form(None),
                     article_id:int=Form(...),
                     approved_status:int=Form(...,description="1->SE approved,2-CE Approved,3-On Hold"),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,4,5]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            
            approvedStatus =["new","SE approved","CE Approved","On Hold"]
            
            journalistEmail = getArticle.createdBy.email if getArticle.created_by else None

            if user.user_type==4:
                getArticle.content_approved = approved_status
                getArticle.chief_editor_id =user.id

                if approved_status in [2,3]:
                    comment = f"The Article Content is {approvedStatus[approved_status]}" if not comment else comment

                    subject ="Artcle Update"
                    mailForArticleUpdate =await send_mail_req_approval(
                    db,subject,comment,journalistEmail
                    )

            if user.user_type==5:
                getArticle.content_approved = approved_status
                getArticle.sub_editor_id =user.id

                if approved_status in [3]:
                    journalistEmail = getArticle.createdBy.email if getArticle.created_by else None
                    comment = f"The Article Content is {approvedStatus[approved_status]}" if not comment else comment

                    subject ="Artcle Update"
                    mailForArticleUpdate = await send_mail_req_approval(
                    db,subject,comment,journalistEmail
                    )

            if user.user_type in [1,2]:
                getArticle.content_approved = approved_status

            db.commit()

            if comment:
                getArticle.comment = comment
                db.commit()


            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f"The Article Content is {approvedStatus[approved_status]}" if not comment else comment,
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 0 if user.user_type==5 else 1,
                chief_editor_notify =(0 if user.user_type==4 else (1
                                       if user.user_type in [1,2,3,5] and approved_status==1 else None)),
                journalist_notify = 1,
                status=1,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id
            )
            db.add(addHistory)
            db.commit()


            return {"status":1,"msg":"Article content approval updated successfully"}

        else:
            return {'status':0,"msg":"You are not authenticated to update content approval."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    



@router.post("/list_article_history")
async def listArticleHistoryHistory(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       article_id:int=Form(None),
                       journalist_id:int=Form(None),
                       sub_editor_id:int=Form(None),
                       chief_editor_id:int=Form(None),
                       page:int=1,size:int = 10):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllArticleHistory = db.query(ArticleHistory).filter(ArticleHistory.status ==1)

            if sub_editor_id:
                getAllArticleHistory = getAllArticleHistory.filter(ArticleHistory.sub_editor_id==sub_editor_id)

            if journalist_id:
                getAllArticleHistory = getAllArticleHistory.filter(ArticleHistory.journalist_id==journalist_id)

            if article_id:
                getAllArticleHistory = getAllArticleHistory.filter(ArticleHistory.article_id==article_id)

            if chief_editor_id:
                getAllArticleHistory = getAllArticleHistory.filter(ArticleHistory.chief_editor_id==chief_editor_id)


            totalCount = getAllArticleHistory.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllArticleHistory = getAllArticleHistory.limit(limit).offset(offset).all()

            dataList=[]

            if getAllArticleHistory:
                for row in getAllArticleHistory:
                    dataList.append({
                "article_history_id":row.id,
                "comment":row.comment,
                "journalist_id":row.journalist_id,
                "journalist_name":row.journalistUser.user_name if row.journalist_id else None,
                "chief_editor_id":row.chief_editor_id,
                "chief_editor_name":row.chiefEditerUser.user_name if row.chief_editor_id else None,
                "sub_editor_id":row.sub_editor_id,
                "sub_editor_name":row.subEditerUser.user_name if row.sub_editor_id else None,
 
                "created_at":row.created_at,                  
                "created_by":row.createdBy.user_name if row.created_by else None,                  
                      }  )
            
            data=({"page":page,"size":size,
                   "total_page":totalPages,
                   "total_count":totalCount,
                   "items":dataList})
        
            return ({"status":1,"msg":"Success","data":data})
        else:
            return {'status':0,"msg":"You are not authenticated to view ArticleHistory."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})