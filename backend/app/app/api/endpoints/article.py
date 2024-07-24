from fastapi import APIRouter, Depends, Form,requests,UploadFile,File
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime,date
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
                   content:str=Form(None),
                   meta_title:str=Form(None),
                   submition_date:date=Form(None),
                   meta_description:str=Form(None),
                   meta_keywords:str=Form(None),
                   seo_url:str=Form(None),
                   category_id:int=Form(...),
                   sub_category_id:int=Form(...),
                   city_id:int=Form(...),
                   state_id:int=Form(...),
                #    article_files: Optional[List[UploadFile]] = File(None),
                   img_alter:str=Form(None),
                   ):
    
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user.user_type !=8:

            addArticle = Article(
                topic=topic,
                content=content,
                meta_title=meta_title,
                submition_date=submition_date,
                meta_description=meta_description,
                img_alter=img_alter,
                meta_keywords=meta_keywords,
                seo_url=seo_url,
                category_id=category_id,
                content_approved=3 if user.user_type!=8 else 0,
                topic_approved=3 if user.user_type!=8 else 0,
                sub_category_id=sub_category_id,
                city_id=city_id,
                state_id=state_id,
                status=1,
                created_by = user.id,
                created_at = datetime.now(settings.tz_IN)
            )
            db.add(addArticle)
            db.commit()
            if user.user_type==8:

                addHistory = ArticleHistory(
                    article_id = addArticle.id,
                    comment = "The Article Topic is Send for Approval",
                    journalist_id = addArticle.created_by ,
                    sub_editor_notify = 1,
                    chief_editor_notify =0,
                    journalist_notify = 0,
                    status=1,
                    created_at =datetime.now(settings.tz_IN),
                    created_by = user.id
                )
                db.add(addHistory)
                db.commit()

            # if article_files :
            #     row = 0
            #     imageData =[]
            #     for file in article_files:
            #         uploadedFile = file.filename
            #         fName,*etn = uploadedFile.split(".")
            #         filePath,returnFilePath = file_storage(file,fName)

            #         imageData.append({
            #             "img_path" : returnFilePath,
            #             "img_alter" : img_alter,
            #             "created_at" : datetime.now(settings.tz_IN),
            #             "status" : 1,
            #             "article_id":addArticle.id,
            #             "created_by":user.id
            #         })
            #         row += 1
                
            #     try:
            #         with db as conn:
            #             conn.execute(ArticleFiles.__table__.insert().values(imageData))
            #             conn.commit()
            #     except Exception as e:
            #         addArticle.status=-1
            #         db.commit()
            #         print(f"Error during bulk insert: {str(e)}")
            #         return ({"status":0,"msg":"Error during article creation"})

        return ({"status":1,"msg":"Successfully New Article Published. ","article_id":addArticle.id})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/delete_article")
async def deleteArticle(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     article_id:int=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2] :
            getArticle = db.query(Article).filter(Article.id == article_id,
                                            Article.status == 1)
            
            getArticle = getArticle.update({"status":-1})
            db.commit()
            return {"status":1,"msg":"Article successfully deleted."}
        else:
            return {'status':0,"msg":"You are not authenticated to delete any user"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
@router.post("/update_article")
async def updateArticle(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   article_id:int=Form(...),
                   topic:str=Form(...),
                   content:str=Form(...),
                   meta_title:str=Form(None),
                   submition_date:date=Form(None),
                   meta_description:str=Form(None),
                   meta_keywords:str=Form(None),
                   seo_url:str=Form(None),
                   city_id:int=Form(...),
                   state_id:int=Form(...),
                #    article_files: Optional[List[UploadFile]] = File(None),
                   img_alter:str=Form(None),
                   ):
    
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user.user_type !=8:

            getArticle = db.query(Article).filter(Article.id==article_id,
                                            Article.status==1).first()

            if not getArticle:
                return {"status":0,"msg":"Article Not Found"}
            
            getArticle.topic=topic
            getArticle.img_alter=img_alter
            getArticle.content=content
            getArticle.meta_title=meta_title
            getArticle.meta_description=meta_description
            getArticle.meta_keywords=meta_keywords
            getArticle.seo_url=seo_url
            getArticle.submition_date=submition_date
            # getArticle.content_approved=2
            # getArticle.topic_approved=2
            getArticle.city_id=city_id
            getArticle.state_id=state_id
            getArticle.status=1
            getArticle.updated_by = user.id
            getArticle.updated_at = datetime.now(settings.tz_IN)
            db.commit()

            # if article_files :

            #     delFiles = db.query(ArticleFiles).\
            #         filter(ArticleFiles.article_id==getArticle.id).update({"status":-1})
                
            #     db.commit()

            #     row = 0
            #     imageData =[]
            #     for file in article_files:
            #         uploadedFile = file.filename
            #         fName,*etn = uploadedFile.split(".")
            #         filePath,returnFilePath = file_storage(file,fName)

            #         imageData.append({
            #             "img_path" : returnFilePath,
            #             "img_alter" : img_alter,
            #             "created_at" : datetime.now(settings.tz_IN),
            #             "status" : 1,
            #             "article_id":getArticle.id,
            #             "created_by":user.id
            #         })
            #         row += 1
                
            #     try:
            #         with db as conn:
            #             conn.execute(ArticleFiles.__table__.insert().values(imageData))
            #             conn.commit()
            #     except Exception as e:

            #         print(f"Error during bulk insert: {str(e)}")
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
    
@router.post("/list_deadline_article")
async def listDeadlineArticle(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       category_id:int=Form(None),
                       city_id:int=Form(None),
                       state_id:int=Form(None),
                       sub_category_id:int=Form(None),
                       journalist_id:int=Form(None),
                    #    topic_approval_status:int=Form(None,description="0-not submitted,1->new,2->SE approved,3-CE Approved,4-On Hold"),
                    #    contant_approval_status:int=Form(None,description="0-not submitted,1->new,2->SE approved,3-CE Approved,4-On Hold"),
                       page:int=1,size:int = 10):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user.user_type in [1,2,3]:
            getDeadlineArticles = db.query(Article).filter(
                    Article.status==1,
                    Article.content_approved==0,
                    Article.submition_date<=datetime.now(settings.tz_IN)
                )
            if state_id:
                getDeadlineArticles = getDeadlineArticles.filter(Article.state_id==state_id)
            if journalist_id:
                getDeadlineArticles = getDeadlineArticles.filter(Article.created_by==journalist_id)
            if city_id:
                getDeadlineArticles = getDeadlineArticles.filter(Article.city_id==city_id)

            if category_id:
                getDeadlineArticles = getDeadlineArticles.filter(Article.category_id==category_id)

            if sub_category_id:
                getDeadlineArticles = getDeadlineArticles.filter(Article.sub_category_id==sub_category_id)

            # if topic_approval_status:
            #     getDeadlineArticles = getDeadlineArticles.filter(Article.topic_approved==topic_approval_status)

            # if contant_approval_status:
                
            #     getDeadlineArticles = getDeadlineArticles.filter(Article.content_approved==contant_approval_status)

            totalCount = getDeadlineArticles.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getDeadlineArticles = getDeadlineArticles.limit(limit).offset(offset).all()

            dataList=[]

            stsName = ["Not submitted","new","SE approved","CE Approved","Approved","On Hold"]
            if getDeadlineArticles:
                for row in getDeadlineArticles:
                        dataList.append({
                "article_id":row.id,
                "meta_title":row.meta_title,
                "meta_description":row.meta_description,
                "category_id":row.category_id,
                "sub_category_id":row.sub_category_id,
                "topic":row.topic,
                "seo_url":row.seo_url,
                "img_alter":row.img_alter,
                "content":row.content,
                 "state_id":row.state_id,
                "state_name":row.states.name if row.state_id else None,
                "city_id":row.city_id,
                "is_journalist":row.is_journalist,
                "city_name":row.cities.name if row.city_id else None,
                "submition_date":row.submition_date,
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
            
            data=({"page":page,"size":size,
                   "total_page":totalPages,
                   "total_count":totalCount,
                   "items":dataList})
        
            return ({"status":1,"msg":"Success","data":data})
        else:
            return {'status':0,"msg":"You are not authenticated to view Deadline Article."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
    
    
@router.post("/list_article")
async def listArticle(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       category_id:int=Form(None),
                       city_id:int=Form(None),
                       state_id:int=Form(None),
                       sub_category_id:int=Form(None),
                       journalist_id:int=Form(None),
                       section_type:int=Form(None,description="1-Topic,2-Content"),

                       article_status:int=Form(None,description="1-new,2-waiting for approval,3-onhold"),

                    #    topic_approval_status:int=Form(None,description="0-not submitted,1->new,2->SE approved,3-CE Approved,4-On Hold"),
                    #    contant_approval_status:int=Form(None,description="0-not submitted,1->new,2->SE approved,3-CE Approved,4-On Hold"),
                       page:int=1,size:int = 10):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllArticle = db.query(Article).filter(Article.status ==1)

            if state_id:
                getAllArticle = getAllArticle.filter(Article.state_id==state_id)
            if journalist_id:
                getAllArticle = getAllArticle.filter(Article.created_by==journalist_id)
            if city_id:
                getAllArticle = getAllArticle.filter(Article.city_id==city_id)

            if category_id:
                getAllArticle = getAllArticle.filter(Article.category_id==category_id)

            if sub_category_id:
                getAllArticle = getAllArticle.filter(Article.sub_category_id==sub_category_id)

            if not article_status:
                getAllArticle = getAllArticle.filter(and_(Article.topic_approved==3,
                                                          Article.content_approved==3,
                ))

            # approval_pending = db.query(Article).filter(Article.status==1,or_(Article.topic_approved!=3,
            #                                               Article.content_approved.not_in([0,3]),
            #     ))
            
            approval_pending = db.query(Article).filter(Article.status==1,or_(Article.topic_approved==4,
                                                          Article.content_approved==4),
                )
            
            if user.user_type==8:
                approval_pending =approval_pending.filter(Article.created_by==user.id)

            approval_pending =approval_pending.count()

            if (article_status!=2 and article_status) and not section_type:

                articleSts =[4 if article_status==3 else article_status ]

                if article_status==1:
                    articleSts = [0,1,2]


                getAllArticle = getAllArticle.filter(or_(Article.topic_approved.in_(articleSts),
                                                     Article.content_approved.in_(articleSts)))
            
            if article_status==2 and section_type:

                
                if section_type==2:

                    getAllArticle = getAllArticle.filter(and_(Article.topic_approved==3,
                                                            #   Article.topic_approved!=4,
                                                              Article.content_approved.not_in([3,4])) )
                    
                if section_type==1:
                    getAllArticle = getAllArticle.filter(
                                                        Article.topic_approved.in_([0,1,2]))
                
                # if section_type==2:
                #     getAllArticle = getAllArticle.filter(
                #                                         Article.content_approved.in_([0,1]))

            # if topic_approval_status:
            #     getAllArticle = getAllArticle.filter(Article.topic_approved==topic_approval_status)

            # if contant_approval_status:
                
            #     getAllArticle = getAllArticle.filter(Article.content_approved==contant_approval_status)

            notifyCount = 0
            deadlineArtcileCount = 0

            getAllNotify = db.query(ArticleHistory).filter(ArticleHistory.status==1)

            if user.user_type in [1,2,3]:
                getDeadlineArticles = db.query(Article).filter(
                    Article.status==1,
                    Article.content_approved==0,
                    Article.submition_date<=datetime.now(settings.tz_IN)
                ).count()
                deadlineArtcileCount = getDeadlineArticles

            if user.user_type ==4:
                getAllNotify = getAllNotify.filter(
                    # ArticleHistory.chief_editor_id==user.id,
                                                   ArticleHistory.chief_editor_notify==1).count()
                notifyCount = getAllNotify

            if user.user_type ==5:
                getAllNotify = getAllNotify.filter(
                    # ArticleHistory.sub_editor_id==user.id,
                                                   ArticleHistory.sub_editor_notify==1).count()
                notifyCount = getAllNotify

            if user.user_type ==8:
                getAllArticle = getAllArticle.filter(Article.created_by==user.id)

                getAllNotify = getAllNotify.filter(ArticleHistory.journalist_id==user.id,
                                                   ArticleHistory.journalist_notify==1).count()
                notifyCount = getAllNotify

            totalCount = getAllArticle.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllArticle = getAllArticle.limit(limit).offset(offset).all()

            dataList=[]

            stsName = ["Not submitted","new","SE approved","CE Approved","Approved","On Hold"]
            if getAllArticle:
                for row in getAllArticle:
                    dataList.append({
                "article_id":row.id,
                "meta_title":row.meta_title,
                "meta_description":row.meta_description,
                "category_id":row.category_id,
                "seo_url":row.seo_url,
                "meta_keywords":row.meta_keywords,
                "sub_category_id":row.sub_category_id,
                "topic":row.topic,
                "img_alter":row.img_alter,
                "content":row.content,
                 "state_id":row.state_id,
                "state_name":row.states.name if row.state_id else None,
                "city_id":row.city_id,
                "is_journalist":row.is_journalist,
                "city_name":row.cities.name if row.city_id else None,
                "submition_date":row.submition_date,
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
            
            data=({"approval_pending":approval_pending,
                   "deadline_article_count":deadlineArtcileCount,
                   "notification_count":notifyCount,"page":page,"size":size,
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
                     approved_status:int=Form(...,description="1->approved,2-On Hold"),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,4,5]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            
            topicApproved = 0
            approvedStatus =["not submitted","new","SE approved","CE Approved","On Hold"]
            
            journalistEmail = getArticle.createdBy.email if getArticle.created_by else None
            journalistName = getArticle.createdBy.name if getArticle.created_by else None

            approvedSts=0

            # msgForCmt = [
            #     "-",  # Placeholder for index 0, not used
            #     "We are pleased to inform you that your topic has been approved. We will proceed with the next steps and provide you with further details shortly.",
            #     "We wanted to let you know that your topic has been put on hold for further review. We will update you once we have more information and are ready to proceed."
            # ]
            msgForCmt = [
                "-",  # Placeholder for index 0, not used
                "We are pleased to inform you that your topic has been approved. We will proceed with the next steps and provide you with further details shortly. Please feel free to reach out if you have any questions.",
                "We wanted to let you know that your topic has been put on hold for further review. We will update you once we have more information and are ready to proceed. Thank you for your patience and understanding."
            ]

            if user.user_type==4:

                approvedSts =3 if approved_status==1 else 4

                getArticle.topic_approved = approvedSts
                getArticle.chief_editor_id =user.id


                comment = f"{msgForCmt[approved_status]}" if not comment else comment

                subject ="Artcle Update"
                mailForArticleUpdate = await send_mail_req_approval(
                db,2,getArticle.id,subject,journalistName,journalistEmail,comment
                )

            if user.user_type==5:

                approvedSts =3 if approved_status==1 else 4

                getArticle.topic_approved = approvedSts
                getArticle.sub_editor_id =user.id


                comment = f"{msgForCmt[approved_status]}" if not comment else comment
                
                if approved_status==2:
                    subject ="Artcle Update"
                    mailForArticleUpdate = await send_mail_req_approval(
                    db,2,getArticle.id,subject,journalistName,journalistEmail,comment
                    )


            if user.user_type in [1,2]:
                approvedSts =3 if approved_status==1 else 4

                getArticle.topic_approved = approvedSts

            db.commit()

            if comment:
                getArticle.comment = comment
                db.commit()

            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f"{approvedStatus[approvedSts]}" if not comment else comment,
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 0 if user.user_type==5 else 1,
                chief_editor_notify =(0 if user.user_type==4 else (1
                                       if user.user_type in [1,2,3,5] else None)),
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
    
@router.post("/journalist_artical_update")
async def journalist_artical_update(db:Session = Depends(deps.get_db),
                     token:str=Form(...),
                     comment : str=Form(None),
                     article_id:int=Form(...),
                     ):
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type==7:
            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            

            addHistory = ArticleHistory(
                article_id = article_id,
                comment =  comment,
                sub_editor_id =getArticle.sub_editor_id,
                chief_editor_id =  getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify =  1,
                chief_editor_notify =0,
                journalist_notify = 0,
                status=1,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id
            )
            db.add(addHistory)
            db.commit()

            return {"status":1,"msg":"Article updated successfully"}

        else:
            return {'status':0,"msg":"You are not authenticated to update article."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/article_content_approve")
async def articleContentApprove(db:Session = Depends(deps.get_db),
                     token:str=Form(...),
                     comment : str=Form(None),
                     article_id:int=Form(...),
                     approved_status:int=Form(None,description="1->approved,2-On Hold"),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,4,5]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            
            approvedStatus =["not submitted","new","SE approved","CE Approved","On Hold"]
            # msgForCmt = [
            #     "-",  # Placeholder for index 0, not used
            #     "We are pleased to inform you that the publication of your article content has been approved! Your hard work and effort have paid off, and we are excited to move forward with publishing your article. \n\nThe next steps involve finalizing the publication details and preparing for the article’s release. We will provide you with further information and any actions needed from your end shortly. \n\nThank you for your contribution and dedication. If you have any questions or need further assistance, please do not hesitate to contact us.\n",
            #     "We wanted to inform you that the publication of your article content has been put on hold. This decision was made to ensure that all necessary details are reviewed thoroughly before proceeding. We understand the importance of this content and want to ensure that it meets our high standards.\n\nWe appreciate your patience and understanding during this process. We will keep you updated on any further developments and let you know once the review is complete. If you have any questions or need additional information, please feel free to reach out.\n\nThank you for your cooperation."
            # ]
            msgForCmt = [
                "-",  # Placeholder for index 0, not used
                "We are pleased to inform you that your article has been approved for publication! Your dedication and effort have been recognized, and we’re excited to move forward with the release. \n\nNext, we will finalize the publication details and prepare for the article’s release. You will receive further information and instructions shortly. \n\nThank you for your hard work and commitment. If you have any questions or need assistance, please feel free to reach out to us.",
                "We wanted to inform you that the publication of your article has been put on hold for further review. This step ensures that all aspects of the content are thoroughly examined to meet our standards. \n\nWe understand the importance of your article and appreciate your patience during this review process. We will keep you updated on the status and notify you once the review is complete. If you have any questions or need additional information, please do not hesitate to contact us.\n\nThank you for your understanding and cooperation."
            ]

            
            journalistEmail = getArticle.createdBy.email if getArticle.created_by else None
            journalistName = getArticle.createdBy.name if getArticle.created_by else None
            approvedSts=0
            if user.user_type==4:

                approvedSts =3 if approved_status==1 else 4

                getArticle.content_approved = approvedSts
                getArticle.chief_editor_id =user.id


                comment = f" {msgForCmt[approved_status]}" if not comment else comment
                

                subject ="Artcle Update"
                mailForArticleUpdate = await send_mail_req_approval(
                db,2,getArticle.id,subject,journalistName,journalistEmail,comment
                )
                

            if user.user_type==5:

                approvedSts =3 if approved_status==1 else 4

                getArticle.content_approved = approvedSts
                getArticle.sub_editor_id =user.id

                comment = f" {msgForCmt[approved_status]} " if not comment else comment


                if approved_status==2:

                    subject ="Artcle Update"
                    mailForArticleUpdate = await send_mail_req_approval(
                    db,2,getArticle.id,subject,journalistName,journalistEmail,comment
                    )
                

            if user.user_type in [1,2]:
                approvedSts =3 if approved_status==1 else 4

                getArticle.content_approved = approvedSts

            db.commit()

            if comment:
                getArticle.comment = comment
                db.commit()

            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f" {approvedStatus[approvedSts]}" if not comment else comment,
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 0 if user.user_type==5 else 1,
                chief_editor_notify =(0 if user.user_type==4 else (1
                                       if user.user_type in [1,2,3,5] else None)),
                journalist_notify = 1,
                status=1,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id
            )
            db.add(addHistory)
            db.commit()


            return {"status":1,"msg":"Article updated successfully"}

        else:
            return {'status':0,"msg":"You are not authenticated to update article."}
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