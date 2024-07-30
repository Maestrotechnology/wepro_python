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

@router.post("/send_topic_request")
async def sendTopicReq(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       topic_id:int=Form(None),
                       topic:str=Form(None),
                       category_id:int=Form(None),
                       description:str=Form(...),
                       submition_date:date=Form(None),
                       ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user:

            getTopic = None

            if topic_id:
                getTopic = db.query(ArticleTopic).\
                filter(ArticleTopic.status==1,ArticleTopic.id==topic_id).first()

                if not getTopic :
                    return {"status":0,"msg":"This Topic is Not available"}
                
            addArticle = Article(
                created_at = datetime.now(settings.tz_IN),
                article_topic_id = topic_id,
                topic = topic if not getTopic else getTopic.topic,
                category_id = category_id,
                description = description if not getTopic else getTopic.description,
                submition_date = submition_date,
                created_by = user.id,
                is_journalist = 1,
                editors_choice = 2 if getTopic else 1,
                status=1,
                topic_approved = 5 if getTopic else 1,
            )

            db.add(addArticle)
            db.commit()
            comment=""
            if not getTopic:
                comment=f"The Article {topic} Topic is Send for Approval"
                addHistory = ArticleHistory(
                        article_id = addArticle.id,
                        comment = comment,
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

            if getTopic:
                comment=f"The Article {addArticle.topic} Topic has been approved."
                addHistory = ArticleHistory(
                        article_id = addArticle.id,
                        comment = comment,
                        journalist_id = addArticle.created_by ,
                        # sub_editor_notify = 1,
                        # chief_editor_notify =0,
                        # journalist_notify = 0,
                        status=1,
                        created_at =datetime.now(settings.tz_IN),
                        created_by = user.id
                    )
                db.add(addHistory)
                db.commit()


            subject ="Artcle Update"
            mailForArticleUpdate = await send_mail_req_approval(
            db,2,addArticle.id,addArticle.created_by,subject,user.name,user.email,comment
            )

            return {"status":1,"msg":comment}
        
        return ({"status":1,"msg":"Successfully New Article Published.","article_id":addArticle.id})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}


@router.post("/create_article")
async def createArticle(db:Session =Depends(deps.get_db),
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
                   img_alter:str=Form(None),
                   ):
    
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user:


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
                is_journalist = 1 if user.user_type==8 else None,
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
                   sub_category_id:int=Form(...),
                   article_title:str=Form(...),
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
        if user.user_type :

            getArticle = db.query(Article).filter(Article.id==article_id,
                                            Article.status==1).first()

            if not getArticle:
                return {"status":0,"msg":"Article Not Found"}
            
            getArticle.article_title=article_title
            getArticle.img_alter=img_alter
            getArticle.content=content
            getArticle.sub_category_id=sub_category_id

            getArticle.meta_title=meta_title
            getArticle.meta_description=meta_description
            getArticle.meta_keywords=meta_keywords
            getArticle.seo_url=seo_url
            getArticle.submition_date=submition_date
            getArticle.city_id=city_id
            getArticle.state_id=state_id
            getArticle.status=1
            getArticle.updated_by = user.id
            getArticle.updated_at = datetime.now(settings.tz_IN)
            db.commit()

         
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
        
        approvedStatus =["-","New","review","comment","Sub Edior Approved","Chief Editor Approved"]
        contentApprovedStatus =["-","New","review","comment","Sub Edior Approved","Chief Editor Approved/Published"]

        data={
            "article_id":getArticle.id,
            "topic":getArticle.topic,
            "editors_choice":getArticle.editors_choice,
            "is_paid":getArticle.is_paid,
            "article_title":getArticle.article_title,
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
            "content_approved": contentApprovedStatus[getArticle.content_approved] if getArticle.content_approved else None,
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
                    Article.content_approved==1,
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

                       article_status:int=Form(None,description="1-new,2-review,3-comment,4-pending all,5-published"),
                       editors_choice:int=Form(None,description="1-no,2-yes"),
                       is_paid :int =Form(None,description="1-pending,2-paid"),\
                       page:int=1,size:int = 10):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllArticle = db.query(Article).filter(Article.status ==1)

            if state_id:
                getAllArticle = getAllArticle.filter(Article.state_id==state_id)
            if is_paid:
                getAllArticle = getAllArticle.filter(Article.is_paid==is_paid)
            if editors_choice:
                getAllArticle = getAllArticle.filter(Article.editors_choice==editors_choice)
            if journalist_id:
                getAllArticle = getAllArticle.filter(Article.created_by==journalist_id)
            if city_id:
                getAllArticle = getAllArticle.filter(Article.city_id==city_id)

            if category_id:
                getAllArticle = getAllArticle.filter(Article.category_id==category_id)

            if sub_category_id:
                getAllArticle = getAllArticle.filter(Article.sub_category_id==sub_category_id)

            # if article_status==4:
            #     getAllArticle = getAllArticle.filter(Article.content_approved!=5)

   
            approval_pending = db.query(Article).filter(Article.status==1,
                                                          Article.content_approved!=5)
            
            if user.user_type==8:
                approval_pending =approval_pending.filter(Article.created_by==user.id)
                getAllArticle = getAllArticle.filter(Article.created_by==user.id)

            approval_pending =approval_pending.count()

            if article_status ==5:

                getAllArticle = getAllArticle.filter(Article.topic_approved==article_status,
                                                     Article.content_approved==article_status)
                
            # if article_status and article_status not in [4,5]:

            #     getAllArticle = getAllArticle.filter(or_(Article.topic_approved==article_status,
            #                                          Article.content_approved==article_status))

            if article_status==1:
                 getAllArticle =getAllArticle.filter(or_(Article.topic_approved==1,
                                                         Article.content_approved==1))
            
                
            if section_type==2 and user.user_type==4:

                getAllArticle = getAllArticle.filter(Article.topic_approved==5,
                                                            Article.content_approved==4)
                
            if section_type==2 and user.user_type==5:
                getAllArticle = getAllArticle.filter(Article.topic_approved==5,
                                                     Article.content_approved.not_in([4,5]))

            if section_type==1 and user.user_type==4:

                getAllArticle = getAllArticle.filter(Article.topic_approved==4 )
                
            if section_type==1 and user.user_type==5:
                getAllArticle = getAllArticle.filter(Article.topic_approved.not_in([4,5]))

    
            notifyCount = 0
            deadlineArtcileCount = 0

            getAllNotify = db.query(ArticleHistory).filter(ArticleHistory.status==1)

            if user.user_type in [1,2,3]:
                getDeadlineArticles = db.query(Article).filter(
                    Article.status==1,
                    Article.content_approved==1,
                    Article.submition_date<=datetime.now(settings.tz_IN)
                ).count()
                deadlineArtcileCount = getDeadlineArticles

            if user.user_type ==4:
                getAllNotify = getAllNotify.filter(
                    ArticleHistory.chief_editor_id==user.id,
                                                   ArticleHistory.chief_editor_notify==1).count()
                notifyCount = getAllNotify

            if user.user_type ==5:
                getAllNotify = getAllNotify.filter(
                    ArticleHistory.sub_editor_id==user.id,
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

            stsName = ["-","new","review","comment","SE Approved","CE Approved","Approved"]
            contentStsName = ["-","new","review","comment","SE Approved","CE Approved","Approved"]
            paymentStatus = ["-","Pending","Paid"]
            if getAllArticle:
                for row in getAllArticle:
                    dataList.append({
                "article_id":row.id,
                "meta_title":row.meta_title,
                "editors_choice":row.editors_choice,
                "is_paid":row.is_paid,

                "meta_description":row.meta_description,
                "category_id":row.category_id,
                "category_title":row.category.title if row.category_id else None,
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
                "content_approved_name":contentStsName[row.content_approved] if row.content_approved else None,
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
                    #  approved_status:int=Form(...,description="1->approved,2-On Hold"),
                    approved_status:int=Form(...,description="2-review,3-comment,4->SE approved,5-CE Approved"),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,4,5]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            
            approvedStatus =["-","new","Review","comment","SE approved","CE Approved/Published",]
            
            journalistEmail = getArticle.createdBy.email if getArticle.created_by else None
            journalistName = getArticle.createdBy.name if getArticle.created_by else None


            msgForCmt = [
                "-",
                "-"
                "Your article is currently under review. Our editorial team is diligently working to ensure the highest quality and relevance of the content. We appreciate your patience during this process.\n\nThank you for your submission and cooperation.",
               "We wanted to inform you that the publication of your article has been put on hold for further review. This step ensures that all aspects of the content are thoroughly examined to meet our standards. \n\nWe understand the importance of your article and appreciate your patience during this review process. We will keep you updated on the status and notify you once the review is complete. If you have any questions or need additional information, please do not hesitate to contact us.\n\nThank you for your understanding and cooperation.",
                "We are delighted to inform you that your article topic has been approved by our Sub Editor. Your article has met our editorial standards and is ready for the next stage. \n\nWe will now proceed with the final steps before publication. Thank you for your dedication and exceptional work. If you have any questions, please feel free to contact us.",
                "We are delighted to inform you that your article topic has been approved by our Chief Editor. Thank you for your dedication and exceptional work. If you have any questions, please feel free to contact us.",

                    ]

            if user.user_type==4:


                getArticle.topic_approved = approved_status
                getArticle.chief_editor_id =user.id
                print(approved_status)


                comment = f"{msgForCmt[approved_status]}" if not comment else comment

            if user.user_type==5:

                getArticle.topic_approved = approved_status
                getArticle.sub_editor_id =user.id
                print(approved_status)
                comment = f"{msgForCmt[approved_status]}" if not comment else comment
                
            if approved_status==2:
                subject ="Artcle Update"
                mailForArticleUpdate = await send_mail_req_approval(
                db,2,getArticle.id,getArticle.created_by,subject,journalistName,journalistEmail,comment
                )

            if user.user_type in [1,2]:

                getArticle.topic_approved = approved_status

            db.commit()

            if comment:
                getArticle.comment = comment
                db.commit()

            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f"{approvedStatus[approved_status]}" if not comment else comment,
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 0 if user.user_type==5 else 1,
                chief_editor_notify =(0 if user.user_type==4 else (1
                                       if user.user_type in [1,2,3,5] and approved_status ==4 else None)),
                journalist_notify = 1,
                status=1,
                is_topic=1,
                topic_status=approved_status,
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
        if user.user_type==8:
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
                     approved_status:int=Form(None,description="2-Review,3-comment,4-SE approved,5-CE Approved/Published"),

                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,4,5]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            
            approvedStatus =["-","new","Review","comment","SE approved","CE Approved/Published",]
            getArticle.content_approved = approved_status

            if approved_status==5:
                getArticle.published_at =datetime.now(settings.tz_IN)


            msgForCmt = [
                "-",
                "-"
                "Your article is currently under review. Our editorial team is diligently working to ensure the highest quality and relevance of the content. We appreciate your patience during this process.\n\nThank you for your submission and cooperation.",
               "We wanted to inform you that the publication of your article has been put on hold for further review. This step ensures that all aspects of the content are thoroughly examined to meet our standards. \n\nWe understand the importance of your article and appreciate your patience during this review process. We will keep you updated on the status and notify you once the review is complete. If you have any questions or need additional information, please do not hesitate to contact us.\n\nThank you for your understanding and cooperation.",
                "We are delighted to inform you that your article has been approved by our Sub Editor. Your article has met our editorial standards and is ready for the next stage. \n\nWe will now proceed with the final steps before publication. Thank you for your dedication and exceptional work. If you have any questions, please feel free to contact us.",
                "We are delighted to inform you that your article has been approved and Published by our Chief Editor. Thank you for your dedication and exceptional work. If you have any questions, please feel free to contact us.",

                    ]

            
            journalistEmail = getArticle.createdBy.email if getArticle.created_by else None
            journalistName = getArticle.createdBy.name if getArticle.created_by else None
            if user.user_type==4:


                getArticle.chief_editor_id =user.id


                comment = f" {msgForCmt[approved_status]}" if not comment else comment
                



            if user.user_type==5:


                getArticle.sub_editor_id =user.id

                comment = f" {msgForCmt[approved_status]} " if not comment else comment



            subject ="Artcle Update"
            mailForArticleUpdate = await send_mail_req_approval(
            db,2,getArticle.id,getArticle.created_by,subject,journalistName,journalistEmail,comment
            )
        

            if user.user_type in [1,2,3]:
                getArticle.content_approved = approved_status

            db.commit()

            if comment:
                getArticle.comment = comment
                db.commit()

            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f" {approvedStatus[approved_status]}" if not comment else comment,
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 0 if user.user_type==5 else 1,
                chief_editor_notify =(0 if user.user_type==4 else (1
                                       if user.user_type in [1,2,3,5]  and approved_status ==4 else None)),
                journalist_notify = 1,
                status=1,
                is_content=1,
                content_status = approved_status,
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



@router.post("/change_payment_status")
async def changePaymentStatus(db:Session=Depends(deps.get_db),
                             token:str=Form(...),article_id:int=Form(...),
                             payment_status:int=Form(...,description="2-paid"),
                             comment:str=Form(None)):
    
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getArticle = db.query(Article).filter(Article.id == article_id,
                                            Article.status == 1).first()
            
            if not getArticle:
                return {"status":0,"msg":"Not found"}

            getUser =db.query(User).filter(User.id==getArticle.created_by).first()

            name =getUser.name if getUser else None
            email =getUser.email if getUser else None


            if payment_status ==2 :
                getArticle.is_paid=payment_status
                db.commit()

                
                message = (
                       f"We are pleased to inform you that your payment for the article '{getArticle.topic}' has been successfully processed and paid. "
                        f"Thank you for your valuable contribution.<br><br>"
                        f"If you have any questions or require further assistance, please do not hesitate to reach out to our support team.<br><br>"
                    
                    )

                if comment:
                    message = comment
            
            subject = "Payment Status"


            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f"Payment Paid" if not comment else comment,
                journalist_id = getArticle.created_by ,
                journalist_notify = 1,
                status=1,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id
            )
            db.add(addHistory)
            db.commit()

            sendNotifyEmail = await send_mail_req_approval(db=db,email_type=6,article_id=getArticle.id,user_id=getUser.id or None,
                receiver_email=email,subject=subject,journalistName=name,
                message=message,
            )
            print(sendNotifyEmail)


            return {"status":1,"msg":"success"}
        else:
            return {'status':0,"msg":"You are not authenticated to change status of any user"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}

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