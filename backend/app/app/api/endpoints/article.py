from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from datetime import datetime,date
from app.utils import *
from sqlalchemy import or_
from fastapi import APIRouter, Depends, Form,UploadFile,File
from typing import Optional


router = APIRouter()




@router.post("/approved_editors_topics")
async def approvedEditorsTopics(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       topic_id:int=Form(None),
                       is_approved:int=Form(...,description="1-approved")
                       ):
    
        
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        getTopic = db.query(ArticleTopic).\
            filter(ArticleTopic.status==1,ArticleTopic.id==topic_id).first()

        if not getTopic :
            return {"status":0,"msg":"This Topic is Not available"}
        
        if is_approved==1:
        
            getTopic.is_approved=2
            getTopic.approved_by=user.id
            db.commit()

            addHistory = ArticleHistory(
                    # comment = f" {approvedStatus[approved_status]}" if not comment else comment,
                comment =f"{user.name}(Chief Editor) approved your {getTopic.topic}"  ,
                title = "Editor Choice",
                sub_editor_id = getTopic.created_by,
                chief_editor_id = user.id,
                suub_editor_notify =1,
                status=1,
                history_type=3,
                is_editor = 1,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id
            )
            db.add(addHistory)
            db.commit()

            addNotification = Notification(
                topic_id = getTopic.id,
                comment =f"The Topic is {getTopic.topic}" ,
                title=f'{user.name}(Chief Editor)-Approved New Topic',
                status=1,
                notification_type=4,
                created_at =datetime.now(settings.tz_IN),
                admin_notify=1,
                created_by = user.id

                )
            db.add(addNotification)
            db.commit()


            return {"status":1,"msg":"Successfully ArticleTopic Added"}


    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    
@router.post("/choose_editors_topics")
async def chooseEditorsTopics(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       topic_id:int=Form(None),
                       ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user:

            getTopic = db.query(ArticleTopic).\
            filter(ArticleTopic.status==1,ArticleTopic.id==topic_id).first()

            if not getTopic :
                return {"status":0,"msg":"This Topic is Not available"}
                
            addArticle = Article(
                created_at = datetime.now(settings.tz_IN),
                article_topic_id = topic_id,
                topic =getTopic.topic,
                category_id =  getTopic.category_id,
                sub_category_id =  getTopic.sub_category_id,
                description =  getTopic.description,
                # submition_date = submition_date,
                created_by = user.id,
                is_journalist = 1,
                editors_choice = 2 ,
                status=1,
                topic_approved = 4 ,
                topic_se_approved = 4 ,
                content_se_approved=1
                # topic_ce_approved_at = datetime.now(settings.tz_IN)
                # content_approved = 1 if getTopic else None
                
            )

            db.add(addArticle)
            db.commit()
            
            getTopic.is_choosed=1
            db.commit()
           
            comment=f"The Editors choice {addArticle.topic} Topic has been approved."
            addHistory = ArticleHistory(
                        article_id = addArticle.id,
                        comment = comment,
                        title = "Editors Topic",
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


            # subject ="Artcle Update"
            # mailForArticleUpdate = await send_mail_req_approval(
            # db,2,addArticle.id,addArticle.created_by,subject,user.name,user.email,comment
            # )

            return {"status":1,"msg":comment}
        
        return ({"status":1,"msg":"Successfully New Article Published.","article_id":addArticle.id})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}
    
@router.post("/send_topic_request")
async def sendTopicReq(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       topic_id:int=Form(None),
                       topic:str=Form(None),
                       category_id:int=Form(None),
                       sub_category_id:int=Form(...),
                       description:str=Form(None),
                    #    submition_date:date=Form(None),
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
                category_id = category_id if not getTopic else getTopic.category_id,
                sub_category_id = sub_category_id if not getTopic else getTopic.sub_category_id,
                description = description if not getTopic else getTopic.description,
                topic_se_approved=1,
                # submition_date = submition_date,
                created_by = user.id,
                is_journalist = 1,
                editors_choice = 2 if getTopic else 1,
                status=1,
                # content_approved = 1 if getTopic else None
                
            )

            db.add(addArticle)
            db.commit()

            if getTopic:
                addArticle.topic_ce_approved_at = datetime.now(settings.tz_IN)
                db.commit()

            comment=""
            if not getTopic:
                comment=f"The Article {addArticle.topic} Topic is Send for Approval"
                addHistory = ArticleHistory(
                        article_id = addArticle.id,
                        comment = comment,
                        journalist_id = addArticle.created_by ,
                        title = f"{user.name} Topic Requested",
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
                        title = "Editor Topic",
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
        else:
        
            return {"status":-1,"msg":"Your login session expires.Please login again."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}


@router.post("/topic_request_update")
async def topicReqUpdate(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       topic_request_id:int=Form(...),
                       topic_id:int=Form(None),
                       topic:str=Form(None),
                       category_id:int=Form(...),
                       description:str=Form(None),
                       sub_category_id:int=Form(...),

                    #    submition_date:date=Form(None),
                       ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user:

            getTopic = None

            getArticle = db.query(Article).\
                filter(Article.status==1,Article.id==topic_request_id).first()

            if not getArticle :
                    return {"status":0,"msg":"This Topic Req is Not available"}
            
            getTopic = None

            if topic_id:
                getTopic = db.query(ArticleTopic).\
                filter(ArticleTopic.status==1,ArticleTopic.id==topic_id).first()

                if not getTopic :
                    return {"status":0,"msg":"This Topic is Not available"}
                

            getArticle.updated_at = datetime.now(settings.tz_IN)
            getArticle.article_topic_id = topic_id
            getArticle.topic = topic if not getTopic else getTopic.topic
            getArticle.category_id = category_id if not getTopic else getTopic.category_id
            getArticle.sub_category_id = sub_category_id if not getTopic else getTopic.sub_category_id
            getArticle.description = description if not getTopic else getTopic.description
            getArticle.created_by = user.id
            getArticle.is_journalist = 1
            getArticle.editors_choice = 2 if getTopic else 1
            getArticle.status=1
            # getArticle.content_approved = 1 if getTopic else None

            getArticle.topic_se_approved = 5 if getTopic else 1
            
            db.commit()
            comment=""
            if not getTopic:
                comment=f"The Article {topic} Topic is Send for Approval"

                addHistory = ArticleHistory(
                        article_id = getArticle.id,
                        comment = comment,
                        title = f"{user.name} Topic Requested",

                        journalist_id = getArticle.created_by ,
                        sub_editor_notify = 1,
                        chief_editor_notify =0,
                        sub_editor_id =  getArticle.sub_editor_id,
                        chief_editor_id =  getArticle.chief_editor_id,
                        journalist_notify = 0,
                        status=1,
                        created_at =datetime.now(settings.tz_IN),
                        created_by = user.id
                    )
                db.add(addHistory)
                db.commit()

            if getTopic:
                getArticle.topic_ce_approved_at = datetime.now(settings.tz_IN)
                db.commit()

                comment=f"The Article {getArticle.topic} Topic has been approved."
                addHistory = ArticleHistory(
                        article_id = getArticle.id,
                        comment = comment,
                        title = "Editor Topic",
                        journalist_id = getArticle.created_by ,
                        sub_editor_notify = 1,
                        sub_editor_id =  getArticle.sub_editor_id,
                        chief_editor_id =  getArticle.chief_editor_id,
                        chief_editor_notify =0,
                        journalist_notify = 0,
                        status=1,
                        created_at =datetime.now(settings.tz_IN),
                        created_by = user.id
                    )
                db.add(addHistory)
                db.commit()


            subject ="Artcle Update"
            mailForArticleUpdate = await send_mail_req_approval(
            db,2,getArticle.id,getArticle.created_by,subject,user.name,user.email,comment
            )

            return {"status":1,"msg":comment}
        
        return ({"status":1,"msg":"Successfully New Article Published.","article_id":getArticle.id})
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}

@router.post("/create_article")
async def createArticle(db:Session =Depends(deps.get_db),
                   token:str=Form(...),
                   topic:str=Form(None),
                   topic_id:str=Form(None),
                   middle_content:str=Form(None),
                   footer_content:str=Form(None),
                   header_content:str=Form(None),
                   article_title:str=Form(...),
                   meta_title:str=Form(None),
                   youtube_link:str=Form(None),
                   submition_date:date=Form(None),
                   meta_description:str=Form(None),
                   meta_keywords:str=Form(None),
                   seo_url:str=Form(None),
                   category_id:int=Form(...),
                   sub_category_id:int=Form(None),
                   city_id:int=Form(...),
                   state_id:int=Form(...),
                   img_alter:str=Form(None),
                   media_file:Optional[UploadFile] = File(None),

                   ):
    
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user:

            existSeo = db.query(Article).filter(Article.status==1,
                                                Article.seo_url==seo_url).first()
            
            if existSeo:
                return {"status":0,"msg":"The SEO url must be unique"}


            addArticle = Article(
                topic=topic,
                youtube_link=youtube_link,
                middle_content=middle_content,
                header_content=header_content,
                footer_content=footer_content,
                article_title=article_title,
                meta_title=meta_title,
                submition_date=submition_date,
                meta_description=meta_description,
                img_alter=img_alter,
                meta_keywords=meta_keywords,
                seo_url=seo_url,
                category_id=category_id,
                content_approved=5 if user.user_type!=8 else 0,
                topic_approved=5 if user.user_type!=8 else 0,
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


            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                addArticle.img_path = returnFilePath

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
                   sub_category_id:int=Form(None),
                   article_title:str=Form(...),
                   middle_content:str=Form(None),
                   youtube_link:str=Form(None),
                   footer_content:str=Form(None),
                   header_content:str=Form(None),
                   meta_title:str=Form(None),
                   submition_date:date=Form(None),
                   meta_description:str=Form(None),
                   meta_keywords:str=Form(None),
                   seo_url:str=Form(None),
                   save_for_later:int=Form(None),
                   city_id:int=Form(...),
                   state_id:int=Form(...),
                     media_file:Optional[UploadFile] = File(None),
                #    article_files: Optional[List[UploadFile]] = File(None),
                   img_alter:str=Form(None),
                   ):
    
    user = deps.get_user_token(db=db,token=token)

    if user:
        if user.user_type :

            existSeo = db.query(Article).filter(Article.status==1,
                                                Article.id!=article_id,
                                                Article.seo_url==seo_url).first()
            
            if existSeo:
                return {"status":0,"msg":"The SEO url must be unique"}
            

            getArticle = db.query(Article).filter(Article.id==article_id,
                                            Article.status==1).first()

            if not getArticle:
                return {"status":0,"msg":"Article Not Found"}
            
            print(getArticle.content_approved)
            
            # if user.user_type==8 and (getArticle.topic_approved not in [1,3] or getArticle.content_approved not in [1,3]):
            #     return {"status":0,"msg":"You are not allowed to update during the article review period."}

            
            getArticle.article_title=article_title
            getArticle.youtube_link=youtube_link
            getArticle.img_alter=img_alter
            getArticle.header_content=header_content
            getArticle.middle_content=middle_content
            getArticle.footer_content=footer_content
            getArticle.sub_category_id=sub_category_id

            getArticle.meta_title=meta_title
            getArticle.meta_description=meta_description
            getArticle.meta_keywords=meta_keywords
            getArticle.seo_url=seo_url
            getArticle.submition_date=submition_date
            getArticle.city_id=city_id
            getArticle.state_id=state_id
            getArticle.status=1
            getArticle.save_for_later=save_for_later
            if not save_for_later:
                getArticle.content_se_approved =1 if getArticle.content_approved !=5 else 5
            getArticle.updated_by = user.id
            getArticle.updated_at = datetime.now(settings.tz_IN)
            getArticle.content_created_at = datetime.now(settings.tz_IN) if getArticle.content_created_at ==None else  getArticle.content_created_at
            db.commit()

            if media_file:

                uploadedFile = media_file.filename
                fName,*etn = uploadedFile.split(".")
                filePath,returnFilePath = file_storage(media_file,fName)
                getArticle.img_path = returnFilePath

                db.commit()

            if not save_for_later:

                addHistory = ArticleHistory(
                    article_id = article_id,
                    comment =  f"Edit the {getArticle.topic} artcile content",
                    title=f"{user.name} -content update",
                    sub_editor_id =getArticle.sub_editor_id,
                    chief_editor_id =  getArticle.chief_editor_id,
                    journalist_id = getArticle.created_by ,
                    sub_editor_notify =  1 ,
                    chief_editor_notify =0,
                    journalist_notify = 0,
                    status=1,
                    created_at =datetime.now(settings.tz_IN),
                    created_by = user.id
                )
                db.add(addHistory)
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
                "file_type":eachFile.file_type,
            })
        
        approvedStatus =["-","New","review","comment","Approved","Chief Editor Approved"]
        contentApprovedStatus =["-","New","review","comment","Approved","Chief Editor Approved/Published"]

        data={
            "article_id":getArticle.id,
            "save_for_later":getArticle.save_for_later,
            "article_id":getArticle.id,
            "topic":getArticle.topic,
            "editors_choice":getArticle.editors_choice,
            "is_paid":getArticle.is_paid,
            "media_file":f'{settings.BASE_DOMAIN}{getArticle.img_path}',
            "youtube_link":getArticle.youtube_link,


            "article_title":getArticle.article_title,
            "header_content":getArticle.header_content,
            "footer_content":getArticle.footer_content,
            "middle_content":getArticle.middle_content,
            "article_title":getArticle.article_title,
            "sub_category_title":getArticle.sub_category.title if getArticle.sub_category_id else None,
            "sub_category_id":getArticle.sub_category_id,
            "category_id":getArticle.category_id,
            "category_title":getArticle.category.title if getArticle.category_id else None,


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
             "topic_se_approved": approvedStatus[getArticle.topic_se_approved] if getArticle.topic_se_approved else None,
            "content_se_approved": contentApprovedStatus[getArticle.content_se_approved] if getArticle.content_se_approved else None,
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
    


    
@router.post("/article_topic_approve")
async def articleTopicApprove(db:Session = Depends(deps.get_db),
                     token:str=Form(...),
                     comment : str=Form(None),
                     article_id:int=Form(...),
                    submition_date:date=Form(None),
                    #  approved_status:int=Form(...,description="1->approved,2-On Hold"),
                    approved_status:int=Form(...,description="2-review,3-comment,4->Approved"),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,4,5]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            
            if approved_status==2:
                if user.user_type==4:
                    getArticle.topic_ce_review_at=datetime.now(settings.tz_IN)
                if user.user_type==5:
                    getArticle.topic_se_review_at=datetime.now(settings.tz_IN)

            if approved_status==3:
                if user.user_type==4:
                    getArticle.topic_ce_cmnt_at=datetime.now(settings.tz_IN)
                if user.user_type==5:
                    getArticle.topic_se_cmnt_at=datetime.now(settings.tz_IN)
                
            if approved_status==4:
                if user.user_type==5:

                    getArticle.topic_se_approved_at=datetime.now(settings.tz_IN)
                    getArticle.topic_Approved=1
                if user.user_type==4:

                    getArticle.topic_ce_approved_at=datetime.now(settings.tz_IN)

            getArticle.updated_by =user.id


            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            
            approvedStatus =["-","new","Review","comment","Approved","CE Approved/Published",]

            getArticle.updated_at = datetime.now(settings.tz_IN)

            if submition_date:
                getArticle.submition_date = submition_date
            
            journalistEmail = getArticle.createdBy.email if getArticle.created_by else None
            journalistName = getArticle.createdBy.name if getArticle.created_by else None

            userType = "Chief" if user.userType==4 else "Sub"


            msgForCmt = [
                "-",
                "-",
                "Your article is currently under review. Our editorial team is diligently working to ensure the highest quality and relevance of the content. We appreciate your patience during this process.\n\nThank you for your submission and cooperation.",
               "We wanted to inform you that the publication of your article has been put on hold for further review. This step ensures that all aspects of the content are thoroughly examined to meet our standards. \n\nWe understand the importance of your article and appreciate your patience during this review process. We will keep you updated on the status and notify you once the review is complete. If you have any questions or need additional information, please do not hesitate to contact us.\n\nThank you for your understanding and cooperation.",
                f"We are delighted to inform you that your article topic has been approved by our {userType} Editor. Your article has met our editorial standards and is ready for the next stage. \n\nWe will now proceed with the final steps before publication. Thank you for your dedication and exceptional work. If you have any questions, please feel free to contact us.",
                "We are delighted to inform you that your article topic has been approved by our Chief Editor. Thank you for your dedication and exceptional work. If you have any questions, please feel free to contact us.",

                    ]

            if user.user_type==4:
                getArticle.chief_editor_id =user.id
                getArticle.topic_approved =approved_status


                comment = f"{msgForCmt[approved_status]}" if not comment else comment

            if user.user_type==5:

                getArticle.topic_se_approved = approved_status
                # getArticle.content_approved =1 if approved_status==5 else None
                getArticle.sub_editor_id =user.id
                comment = f"{msgForCmt[approved_status]}" if not comment else comment
                
            subject ="Artcle Update"
            mailForArticleUpdate = await send_mail_req_approval(
            db,2,getArticle.id,getArticle.created_by,subject,journalistName,journalistEmail,comment
            )

            if user.user_type in [1,2]:

                getArticle.topic_ce_approved = approved_status

            db.commit()

            if comment:
                getArticle.comment = comment
                db.commit()

            userType = "Sub Editor" if user.user_type==5 else "Chief Editor"

            if comment:
                msg= comment
            else:
                msg=f" {userType} changed status to {approvedStatus[approved_status]}"
            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f"{userType}-{msg}",
                title= f'{user.name}-Change Topic Status ',
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 0 if user.user_type==5 else 1,
                chief_editor_notify =(0 if user.user_type==4 else (1
                                       if user.user_type in [1,2,3,5] and approved_status ==4 else None)),
                journalist_notify = 1,
                status=1,
                history_type=2,
                is_editor = 1 if user.user_type==5 else 2,
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
                     approved_status:int=Form(None,description="2-Review,3-comment,4- approved"),

                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,4,5]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            

            if approved_status==2:
                if user.user_type==4:
                    getArticle.content_ce_review_at=datetime.now(settings.tz_IN)
                    getArticle.content_approved = approved_status

                if user.user_type==5:
                    getArticle.content_se_review_at=datetime.now(settings.tz_IN)
                    getArticle.content_se_approved = approved_status


            getArticle.updated_by =user.id

            if approved_status==3:
                if user.user_type==4:
                    getArticle.content_ce_cmnt_at=datetime.now(settings.tz_IN)
                    getArticle.content_approved = approved_status
                    
                if user.user_type==5:
                    getArticle.content_se_cmnt_at=datetime.now(settings.tz_IN)
                    getArticle.content_se_approved = approved_status


            if approved_status==4:
                if user.user_type==4:
                    getArticle.content_se_approved = approved_status
                    getArticle.content_se_approved_at=datetime.now(settings.tz_IN)
                if user.user_type==5:
                    getArticle.published_at=datetime.now(settings.tz_IN)
                    getArticle.content_approved = approved_status

            
            getArticle.updated_at = datetime.now(settings.tz_IN)

            
            approvedStatus =["-","new","Review","comment","approved","CE Approved/Published",]

            userType = "Chief" if user.userType==4 else "Sub"


            msgForCmt = [
                "-",
                "-",
                "Your article is currently under review. Our editorial team is diligently working to ensure the highest quality and relevance of the content. We appreciate your patience during this process.\n\nThank you for your submission and cooperation.",
               "We wanted to inform you that the publication of your article has been put on hold for further review. This step ensures that all aspects of the content are thoroughly examined to meet our standards. \n\nWe understand the importance of your article and appreciate your patience during this review process. We will keep you updated on the status and notify you once the review is complete. If you have any questions or need additional information, please do not hesitate to contact us.\n\nThank you for your understanding and cooperation.",
                f"We are delighted to inform you that your article has been approved by our {userType} Editor. Your article has met our editorial standards and is ready for the next stage. \n\nWe will now proceed with the final steps before publication. Thank you for your dedication and exceptional work. If you have any questions, please feel free to contact us.",
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

            userType = "Sub Editor" if user.user_type==5 else "Chief Editor"

            if comment:
                msg=comment
            else:
                msg=f" {userType} changed status to {approvedStatus[approved_status]}"

            addHistory = ArticleHistory(
                article_id = article_id,
                # comment = f" {approvedStatus[approved_status]}" if not comment else comment,
                comment =msg ,
                title= f'{user.name}-Change Content Status ',
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 0 if user.user_type==5 else 1,
                chief_editor_notify =(0 if user.user_type==4 else (1
                                       if user.user_type in [1,2,3,5]  and approved_status ==4 else None)),
                admin_notify = 1 if user.user_type==4 and approved_status==4 else 0,
                journalist_notify = 1,
                status=1,
                history_type=2,
                is_editor = 1 if user.user_type==5 else 2,
                content_status = approved_status,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id
            )
            db.add(addHistory)
            db.commit()

            if user.user_type==4 and approved_status==4 :
                addNotification = Notification(
                article_id = article_id,
                comment =f"Chief Editor Approved {getArticle.topic} article" ,
                title=f'{user.name}(Chief Editor)- Article Approved',
                status=1,
                admin_notify=1,
                notification_type=2,
                content_status = approved_status,
                created_at =datetime.now(settings.tz_IN),
                created_by = user.id

                )
                db.add(addNotification)
                db.commit()


            return {"status":1,"msg":"Article updated successfully"}

        else:
            return {'status':0,"msg":"You are not authenticated to update article."}
    else:
        return {"status":-1,"msg":"Your login session expires.Please login again."}



@router.post("/deadline_reminder")
async def deadlineReminder(db:Session = Depends(deps.get_db),
                     token:str=Form(...),
                     comment : str=Form(None),
                     article_id:int=Form(...),
                     ):
    
    user=deps.get_user_token(db=db,token=token)
    
    if user:
        if user.user_type in [1,2,3,6]:

            getArticle = db.query(Article).filter(Article.status==1,
                                Article.id==article_id).first()
            
            if not getArticle:
                return {"status":0,"msg":"This article is not available."}
            
            getArticle.updated_at = datetime.now(settings.tz_IN)


            msgForCmt = f"Just a quick reminder that the deadline for your article on {getArticle.topic} is coming up on {getArticle.submition_date}. Please make sure to submit it by then to meet our publishing schedule."

            journalistEmail = getArticle.createdBy.email if getArticle.created_by else None
            journalistName = getArticle.createdBy.name if getArticle.created_by else None
          

            subject ="Artcle Update"
            mailForArticleUpdate = await send_mail_req_approval(
            db,2,getArticle.id,getArticle.created_by,subject,journalistName,journalistEmail,comment or msgForCmt
            )

            if comment:
                getArticle.comment = comment
                db.commit()

            addHistory = ArticleHistory(
                article_id = article_id,
                comment = msgForCmt if not comment else comment,
                sub_editor_id = user.id if user.user_type==5 else getArticle.sub_editor_id,
                chief_editor_id = user.id if user.user_type==4 else getArticle.chief_editor_id,
                journalist_id = getArticle.created_by ,
                sub_editor_notify = 1,
                chief_editor_notify =1,
                journalist_notify = 1,
                status=1,
                is_content=1,
                content_status = 6,
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
                             amount:int=Form(...),
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
                getArticle.paid_amount=amount
                db.commit()

                
                message = (
                        f"We are pleased to inform you that your payment of {amount} for the article '{getArticle.topic}' has been successfully processed and paid."
                        f"Thank you for your valuable contribution.<br><br>"
                        f"If you have any questions or require further assistance, please do not hesitate to reach out to our support team.<br><br>"
                    
                    )

                if comment:
                    message = comment
            
            subject = "Payment Status"


            addHistory = ArticleHistory(
                article_id = article_id,
                comment = f"Payment of {amount} paid for the article" if not comment else comment,
                title=f'{user.name}(HR)-Payment Update',
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
    

@router.post("/list_article")
async def listArticle(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       category_id:int=Form(None),
                       city_id:int=Form(None),
                       state_id:int=Form(None),
                       sub_category_id:int=Form(None),
                       journalist_id:int=Form(None),
                       name:str=Form(None),
                       editor_type:int=Form(None,description="1-se,2-ce"),
                       section_type:int=Form(None,description="1-Topic,2-Content"),
                       topic:str=Form(None),
                       article_status:int=Form(None,description="1-new,2-review,3-comment,4-approved"),
                       editors_choice:int=Form(None,description="1-no,2-yes"),
                       is_paid :int =Form(None,description="1-pending,2-paid"),
                       is_deadline:int=Form(None,description="1-list deadline articles"),
                       page:int=1,size:int = 10):
    
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getAllArticle = db.query(Article).filter(Article.status ==1)
            
            if name:
                
                getAllArticle = getAllArticle.join(User,Article.created_by==User.id).filter(User.name.like("%"+name+"%"))
            if topic:
                getAllArticle =  getAllArticle.filter(Article.topic.like("%"+topic+"%"))

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

   
            # approval_pending = db.query(Article).filter(Article.status==1,
            #                                               Article.content_approved!=5)
            # approval_pending =approval_pending.filter(Article.created_by==user.id)

            # approval_pending =approval_pending.count()

            notifyCount = 0
            deadlineArtcileCount = 0
            getAllNotify = db.query(ArticleHistory).filter(ArticleHistory.status==1)



            # if article_status ==5 and not section_type:

            #     getAllArticle = getAllArticle.filter(Article.topic_approved==article_status,
            #                                          Article.content_approved==article_status)
                

            # if article_status==1 and not section_type:
            #      getAllArticle =getAllArticle.filter(or_(Article.topic_approved==1,
            #                                              Article.content_approved==1))
            if user.user_type==4:

                getAllArticle =  getAllArticle.filter(or_(Article.chief_editor_id==user.id,Article.chief_editor_id==None))

                #  get all Chief editor unapproved contents
                
                if section_type==2 and not article_status:

                    getAllArticle = getAllArticle.filter(Article.content_se_approved==4)
                    
                # get All Chief editor unapproved Topic

                if section_type==1 and not article_status:

                    # getAllArticle = getAllArticle.filter(Article.topic_approved==4 )
                    getAllArticle = getAllArticle.filter(Article.topic_se_approved==4,
                                                          Article.editors_choice!=1,
                                                          Article.content_se_approved==None,
                                                        # Article.content_approved.not_in([1,2,3,4,5])
                                                        )
                    
                if section_type==2 and  article_status:

                    getAllArticle = getAllArticle.filter(Article.content_approved==article_status)
                    

                if section_type==1 and  article_status:

                    getAllArticle = getAllArticle.filter(Article.topic_approved==article_status,
                                                        Article.content_se_approved==None# Article.content_approved.not_in([1,2,3,4,5])
                                                        )
                    

                getAllNotify = getAllNotify.filter(
                    ArticleHistory.chief_editor_id==user.id,
                                                   ArticleHistory.chief_editor_notify==1).count()
                notifyCount = getAllNotify


            if user.user_type==5:
                getAllArticle =  getAllArticle.filter(or_(Article.sub_editor_id==user.id,Article.sub_editor_id==None))

                #get all sub editor unapproved content
                
                if section_type==2 and not article_status:
                    getAllArticle = getAllArticle.filter(Article.topic_approved==4)

                    
                # get All sub editor unapproved Topic
                    
                if section_type==1 and not article_status:
                     getAllArticle = getAllArticle.filter(Article.content_se_approved==None,
                                                          Article.topic_se_approved.in_([1,2,3,4]),
                                                          Article.editors_choice!=1,
                                                        )
                
                if section_type==2 and  article_status:

                    getAllArticle = getAllArticle.filter(Article.content_approved==article_status)
                    

                if section_type==1 and  article_status:

                    getAllArticle = getAllArticle.filter(Article.topic_approved==article_status,
                                                        Article.content_se_approved==None,# Article.content_approved.not_in([1,2,3,4,5])
                                                        )
                getAllNotify = getAllNotify.filter(
                    ArticleHistory.sub_editor_id==user.id,
                                                ArticleHistory.sub_editor_notify==1).count()
                notifyCount = getAllNotify


            if user.user_type in [1,2,3]:
                getDeadlineArticles = db.query(Article).filter(
                    Article.status==1,
                    Article.submition_date<=datetime.now(settings.tz_IN)
                ).count()


                # is_deadline->1 show deadline reached article 

                if is_deadline==1:
                     getAllArticle = getAllArticle.filter(
                    Article.submition_date<=datetime.now(settings.tz_IN))
                     

                # list all artcile topic approved but not content approved


                if section_type==2 and not article_status:
                    getAllArticle = getAllArticle.filter(Article.topic_approved==4,
                                                        #  Article.content_approved!=5,
                                                        #    Article.content_approved!=None
                                                                )
                    
                #list artcile topic unapproved

                if section_type==1 and not article_status:
                    getAllArticle = getAllArticle.filter(Article.topic_approved!=4#  Article.created_by=109
                                                                )
                    
                deadlineArtcileCount = getDeadlineArticles

            if user.user_type ==8:
                getAllArticle = getAllArticle.filter(Article.created_by==user.id)

                if section_type==2 and not article_status:
                    getAllArticle = getAllArticle.filter(Article.topic_approved==4,
                                                        #  Article.content_approved!=5, Article.content_approved!=None
                                                        #   Article.content_approved!=None
                                                                )

                if section_type==1 and not article_status:
                    getAllArticle = getAllArticle.filter(Article.topic_approved!=4)
                    
                
                getAllNotify = getAllNotify.filter(ArticleHistory.journalist_id==user.id,
                                                ArticleHistory.journalist_notify==1).count()
                notifyCount = getAllNotify


            # unapproved content article list -status based

            if editor_type:

                if section_type==2 and article_status :
                    if editor_type==1:


                        getAllArticle = getAllArticle.filter(Article.topic_approved==4,
                                                            Article.content_se_approved==article_status,
                                                                    )
                        
                    if editor_type==2:
                        getAllArticle = getAllArticle.filter(Article.topic_approved==4,
                                                            Article.content_approved==article_status,
                                                                    )
            
         

                if section_type==1 and article_status :
                    if editor_type==1:


                        getAllArticle = getAllArticle.filter(Article.content_se_approved==None,
                                                          Article.topic_se_approved==article_status,
                                                          Article.editors_choice!=1)
                        
                    if editor_type==2:
                        getAllArticle =  getAllArticle.filter(Article.topic_se_approved==4,
                                                          Article.editors_choice!=1,
                                                          Article.content_se_approved==None,
                                                        Article.topic_approved==article_status,
                                                        )
             

            totalCount = getAllArticle.count()
            getAllArticle = getAllArticle.order_by(Article.created_at.desc())
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllArticle = getAllArticle.limit(limit).offset(offset).all()

            dataList=[]

            stsName = ["-","new","review","comment","Approved","CE Approved","Approved"]
            contentStsName = ["-","new","review","comment","Approved","CE Approved","Approved"]
            paymentStatus = ["-","Pending","Paid"]
            if getAllArticle:
                for row in getAllArticle:

                    getArticleTop = db.query(ArticleHistory).filter(ArticleHistory.article_id==row.id).first()
                    getArticleCon = db.query(ArticleHistory).filter(ArticleHistory.article_id==row.id).first()

                    topicUserType = getArticleTop.createdBy.user_type if getArticleTop and getArticleTop.created_by else None
                    conUsertype = getArticleCon.createdBy.user_type if getArticleCon and getArticleCon.created_by else None

                    topicUserType="CE" if topicUserType ==4 else "SE" if topicUserType==5 else None 
                    conUsertype="CE" if conUsertype ==4 else "SE" if conUsertype==5 else None 


                    dataList.append({
                "article_id":row.id,
                "paid_amount":row.paid_amount,
                "meta_title":row.meta_title,
                "save_for_later":row.save_for_later,
                "article_title":row.article_title,
                "editors_choice":row.editors_choice,
                "is_paid":row.is_paid,
                "media_file":f'{settings.BASE_DOMAIN}{row.img_path}' if row.img_path else "",

                "meta_description":row.meta_description,
                "description":row.description,
                "category_id":row.category_id,
                "youtube_link":row.youtube_link,
                "category_title":row.category.title if row.category_id else None,
                "seo_url":row.seo_url,
                "meta_keywords":row.meta_keywords,
                "sub_category_id":row.sub_category_id,
                "sub_category_title":row.sub_category.title if row.sub_category_id else None,

                "topic":row.topic,
                "img_alter":row.img_alter,
                "header_content":row.header_content,
                "footer_content":row.footer_content,
                "middle_content":row.middle_content,
                 "state_id":row.state_id,
                "state_name":row.states.name if row.state_id else None,
                "city_id":row.city_id,
                "is_journalist":row.is_journalist,
                "city_name":row.cities.name if row.city_id else None,
                "topic_se_approved_name": stsName[row.topic_se_approved] if row.topic_se_approved else None,
                "content_se_approved_name": stsName[row.content_se_approved] if row.content_se_approved else None,
                "topic_se_approved": row.topic_se_approved ,
                "content_se_approved": row.content_se_approved ,
            
                "submition_date":row.submition_date,
                "topic_approved":row.topic_approved,
                "topic_status_name":stsName[row.topic_approved] if row.topic_approved else None ,
                "content_approved":0 if row.topic_approved==5 and not row.content_approved else row.content_approved ,
                "content_status_name":contentStsName[row.content_approved] if row.content_approved else None,
                "topic_approved_name":f"{getArticleTop.createdBy.user_name}({topicUserType})" if getArticleTop and getArticleTop.created_by else None ,
                "content_approved_name":f"{getArticleCon.createdBy.user_name}({conUsertype})" if getArticleCon and getArticleCon.created_by else None ,
                "created_at":row.created_at,                  
                "updated_at":row.updated_at, 
                "journalist_id":row.created_by,                 
                "journalist_name":row.createdBy.user_name if row.created_by else None,                  
                "updated_by":row.updatedBy.user_name if row.updated_by else None,                  
                      }  )
            
            data=({
                # "approval_pending":approval_pending,
                   "deadline_article_count":deadlineArtcileCount,
                   "notification_count":notifyCount,
                   "page":page,"size":size,
                   "total_page":totalPages,
                   "total_count":totalCount,
                   "items":dataList})
        
            return ({"status":1,"msg":"Success","data":data})
        else:
            return {'status':0,"msg":"You are not authenticated to view Article."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
    



# @router.post("/test_list_article")
# async def test_listArticle(db:Session =Depends(deps.get_db),
#                        token:str = Form(...),
#                        category_id:int=Form(None),
#                        city_id:int=Form(None),
#                        state_id:int=Form(None),
#                        sub_category_id:int=Form(None),
#                        journalist_id:int=Form(None),
#                        section_type:int=Form(None,description="1-Topic,2-Content"),

#                        article_status:int=Form(None,description="1-new,2-review,3-comment,5-published"),
#                        editors_choice:int=Form(None,description="1-no,2-yes"),
#                        is_paid :int =Form(None,description="1-pending,2-paid"),\
#                        page:int=1,size:int = 10):
    
#     user=deps.get_user_token(db=db,token=token)
#     if user:
#         if user:
#             getAllArticle = db.query(Article).filter(Article.status ==1)

#             if state_id:
#                 getAllArticle = getAllArticle.filter(Article.state_id==state_id)
#             if is_paid:
#                 getAllArticle = getAllArticle.filter(Article.is_paid==is_paid)
#             if editors_choice:
#                 getAllArticle = getAllArticle.filter(Article.editors_choice==editors_choice)
#             if journalist_id:
#                 getAllArticle = getAllArticle.filter(Article.created_by==journalist_id)
#             if city_id:
#                 getAllArticle = getAllArticle.filter(Article.city_id==city_id)

#             if category_id:
#                 getAllArticle = getAllArticle.filter(Article.category_id==category_id)

#             if sub_category_id:
#                 getAllArticle = getAllArticle.filter(Article.sub_category_id==sub_category_id)

#             # if article_status==4:
#             #     getAllArticle = getAllArticle.filter(Article.content_approved!=5)

   
#             approval_pending = db.query(Article).filter(Article.status==1,
#                                                           Article.content_approved!=5)
            
#             if user.user_type==8:
#                 approval_pending =approval_pending.filter(Article.created_by==user.id)
#                 getAllArticle = getAllArticle.filter(Article.created_by==user.id)

#             approval_pending =approval_pending.count()


#             if article_status ==5 and not section_type:

#                 getAllArticle = getAllArticle.filter(Article.topic_approved==article_status,
#                                                      Article.content_approved==article_status)
                
#             # if article_status and article_status not in [4,5]:

#             #     getAllArticle = getAllArticle.filter(or_(Article.topic_approved==article_status,
#             #                                          Article.content_approved==article_status))

#             if article_status==1 and not section_type:
#                  getAllArticle =getAllArticle.filter(or_(Article.topic_approved==1,
#                                                          Article.content_approved==1))
#             if user.user_type==4:
                
#                 if section_type==2 and user.user_type==4:

#                     getAllArticle = getAllArticle.filter(Article.topic_approved==5,
#                                                             Article.content_approved==4)
#                 if section_type==1 and user.user_type==4:

#                     getAllArticle = getAllArticle.filter(Article.topic_approved==4 )

#             if user.user_type==5:
                
#                 if section_type==2 and user.user_type==5:
#                     getAllArticle = getAllArticle.filter(Article.topic_approved==5,
#                                                         Article.content_approved.not_in([4,5]))
                    
#                 if section_type==1 and user.user_type==5:
#                     getAllArticle = getAllArticle.filter(Article.topic_approved.not_in([4,5]))

                

    
#             notifyCount = 0
#             deadlineArtcileCount = 0

#             getAllNotify = db.query(ArticleHistory).filter(ArticleHistory.status==1)

#             if user.user_type in [1,2,3]:
#                 getDeadlineArticles = db.query(Article).filter(
#                     Article.status==1,
#                     Article.content_approved==1,
#                     Article.submition_date<=datetime.now(settings.tz_IN)
#                 ).count()
#                 deadlineArtcileCount = getDeadlineArticles

#             if user.user_type ==4:
#                 getAllNotify = getAllNotify.filter(
#                     ArticleHistory.chief_editor_id==user.id,
#                                                    ArticleHistory.chief_editor_notify==1).count()
#                 notifyCount = getAllNotify

#             if user.user_type ==5:
#                 getAllNotify = getAllNotify.filter(
#                     ArticleHistory.sub_editor_id==user.id,
#                                                    ArticleHistory.sub_editor_notify==1).count()
#                 notifyCount = getAllNotify

#             if user.user_type ==8:
#                 getAllArticle = getAllArticle.filter(Article.created_by==user.id)

#                 getAllNotify = getAllNotify.filter(ArticleHistory.journalist_id==user.id,
#                                                    ArticleHistory.journalist_notify==1).count()
#                 notifyCount = getAllNotify

#             totalCount = getAllArticle.count()
#             totalPages,offset,limit = get_pagination(totalCount,page,size)
#             getAllArticle = getAllArticle.limit(limit).offset(offset).all()

#             dataList=[]

#             stsName = ["-","new","review","comment","SE Approved","CE Approved","Approved"]
#             contentStsName = ["-","new","review","comment","SE Approved","CE Approved","Approved"]
#             paymentStatus = ["-","Pending","Paid"]
#             if getAllArticle:
#                 for row in getAllArticle:
#                     dataList.append({
#                 "article_id":row.id,
#                 "meta_title":row.meta_title,
#                 "article_title":row.article_title,
#                 "editors_choice":row.editors_choice,
#                 "is_paid":row.is_paid,
#                 "media_file":f'{settings.BASE_DOMAIN}{row.img_path}',

#                 "meta_description":row.meta_description,
#                 "category_id":row.category_id,
#                 "category_title":row.category.title if row.category_id else None,
#                 "seo_url":row.seo_url,
#                 "meta_keywords":row.meta_keywords,
#                 "sub_category_id":row.sub_category_id,
#                 "topic":row.topic,
#                 "img_alter":row.img_alter,
#                 "header_content":row.header_content,
#                 "footer_content":row.footer_content,
#                 "middle_content":row.middle_content,
#                  "state_id":row.state_id,
#                 "state_name":row.states.name if row.state_id else None,
#                 "city_id":row.city_id,
#                 "is_journalist":row.is_journalist,
#                 "city_name":row.cities.name if row.city_id else None,
#                 "submition_date":row.submition_date,
#                 "topic_approved":row.topic_approved,
#                 "topic_approved_name":stsName[row.topic_approved] if row.topic_approved else None ,
#                 "content_approved":row.content_approved,
#                 "content_approved_name":contentStsName[row.content_approved] if row.content_approved else None,
#                 "created_at":row.created_at,                  
#                 "updated_at":row.updated_at, 
#                 "journalist_id":row.created_by,                 
#                 "journalist_name":row.createdBy.user_name if row.created_by else None,                  
#                 "updated_by":row.updatedBy.user_name if row.updated_by else None,                  
#                       }  )
            
#             data=({"approval_pending":approval_pending,
#                    "deadline_article_count":deadlineArtcileCount,
#                    "notification_count":notifyCount,"page":page,"size":size,
#                    "total_page":totalPages,
#                    "total_count":totalCount,
#                    "items":dataList})
        
#             return ({"status":1,"msg":"Success","data":data})
#         else:
#             return {'status':0,"msg":"You are not authenticated to view Article."}
#     else:
#         return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
