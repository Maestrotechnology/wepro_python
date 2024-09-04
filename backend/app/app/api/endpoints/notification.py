from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from datetime import timedelta
from app.utils import *

router = APIRouter()



@router.post("/notification_count")
async def notificationCount(db:Session=Depends(deps.get_db),
                             token:str=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getNotify = db.query(ArticleHistory).filter(ArticleHistory.status == 1)

            tenDays = datetime.now(settings.tz_IN)-timedelta(days=10)
    
            # deleteOverDueArticle = db.query(Article).filter(Article.status==1,
            #                                     Article.topic_ce_approved_at <= tenDays ,
            #                                     Article.updated_at==None).update({"status":-1}, synchronize_session='fetch')
            # db.commit()

            deleteOverDueArticle = db.query(Article).filter(Article.status==1,
                                                Article.topic_ce_approved_at <= tenDays ,
                                                Article.updated_at==None).all()
            for article in deleteOverDueArticle:
                article.status=-1
                db.commit()
                msg=f"The topic '{article.topic}' has exceeded the timeline, so it has been removed."

                if article.article_topic_id:
                    getArticleTopic = db.query(ArticleTopic).filter(ArticleTopic.id==article.article_topic_id,
                                                                    ArticleTopic.status==1).first()
                    
                    if getArticleTopic:
                        getArticleTopic.is_choosed=0
                        db.commit()

                addHistory = ArticleHistory(
                    article_id = article.id,
                    comment = msg,
                    title= "Topic Removal",
                    sub_editor_id = user.id if user.user_type==5 else article.sub_editor_id,
                    chief_editor_id = user.id if user.user_type==4 else article.chief_editor_id,
                    journalist_id = article.created_by ,
                    sub_editor_notify = 1,
                    chief_editor_notify =1,
                    journalist_notify = 1,
                    status=1,
                    history_type=4,
                    created_at =datetime.now(settings.tz_IN)
                )
                db.add(addHistory)
                db.commit()

            if user.user_type in [1,2]:
                getNotify = db.query(Notification).filter(Notification.status==1,
                                                          Notification.admin_notify==1)
         
                
            if user.user_type==4:
                getNotify=getNotify.filter(ArticleHistory.chief_editor_id==user.id,
                                           ArticleHistory.chief_editor_notify==1)
            if user.user_type==5:
                getNotify=getNotify.filter(ArticleHistory.sub_editor_id==user.id,
                                           ArticleHistory.sub_editor_notify==1)
            if user.user_type==8:
                getNotify=getNotify.filter(ArticleHistory.journalist_id==user.id,
                                           ArticleHistory.journalist_notify==1)
                
            getNotify=getNotify.count()

            message ="Success."


            return {"status":1,"msg":"success","notification_count":getNotify}
        else:
            return {'status':0,"msg":"You are not authenticated to read notification"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
    

@router.post("/list_admin_notification")
async def listAdminNotification(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            
            getAllNotify = db.query(Notification).filter(Notification.status ==1,Notification.admin_notify==1)

            totalCount = getAllNotify.count()

            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllNotify = getAllNotify.order_by(Notification.id.desc()).limit(limit).offset(offset).all()

            notifyTypeName = ["-","Topic","Content","Account Approval","Editor Topic"]

            dataList=[]
            if getAllNotify:
                for row in getAllNotify:
                    dataList.append({
                "notification_id":row.id,
                "comment":row.comment,
                "title":row.title,
                "article_id":row.article_id,
                "notification_type":row.notification_type,
                "notification_type_name":notifyTypeName[row.notification_type] if row.notification_type else None,
                "topic_id":row.topic_id,
                "created_at":row.created_at,                  
                "created_by":row.createdBy.user_name if row.created_by else None,                  
                      }  )
            
            data=({"page":page,"size":size,
                   "total_page":totalPages,
                   "total_count":totalCount,
                   "items":dataList})
        
            return ({"status":1,"msg":"Success","data":data})
        else:
            return {'status':0,"msg":"You are not authenticated to view Notification."}
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})

@router.post("/list_notification")
async def listNotification(db:Session =Depends(deps.get_db),
                       token:str = Form(...),
                       page:int=1,size:int = 10):
    user=deps.get_user_token(db=db,token=token)
    if user:
        if user:
            
            getAllNotify = db.query(ArticleHistory).filter(ArticleHistory.status ==1)

            if user.user_type ==4:
                getAllNotify = getAllNotify.filter(
                    ArticleHistory.chief_editor_id==user.id,
                                                   ArticleHistory.chief_editor_notify==1)

            if user.user_type ==5:
                getAllNotify = getAllNotify.filter(
                    ArticleHistory.sub_editor_id==user.id,
                                                   ArticleHistory.sub_editor_notify==1)

            if user.user_type ==8:
                getAllNotify = getAllNotify.filter(ArticleHistory.journalist_id==user.id,
                                                   ArticleHistory.journalist_notify==1)

            totalCount = getAllNotify.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllNotify = getAllNotify.order_by(ArticleHistory.id.desc()).limit(limit).offset(offset).all()

            historyName = ["-","TOPIC","CONTENT","EDITORS CHOICE"]
            stsName = ["-","new","review","comment","Approved","CE Approved","Approved"]


            dataList=[]
            if getAllNotify:
                for row in getAllNotify:
                    dataList.append({
                "article_history_id":row.id,
                "title":row.title,
                "comment":row.comment,
                "history_type":row.history_type,
                "history_type_name":historyName[row.history_type] if row.history_type else None,
                "article_status":row.content_status if row.history_type==2 else (row.topic_status if row.history_type==1 else None),
                "article_status_name":stsName[row.content_status] if row.history_type==2 and row.content_status else (stsName[row.topic_status] if row.history_type==1 and row.topic_status else None),

                "is_editor":"CE" if row.is_editor==2 else ("CE" if row.is_editor==1 else None),
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


@router.post("/read_notification")
async def readNotification(db:Session=Depends(deps.get_db),
                             token:str=Form(...),notification_id:int=Form(None),
                             read_type:int=Form(...,description="1->read,2->all notify read")):
    user = deps.get_user_token(db=db,token=token)
    if user:
        if user:
            getNotify = db.query(ArticleHistory).filter(ArticleHistory.status == 1)

            if user.user_type in [1,2]:
                getNotify = db.query(Notification).filter(Notification.status==1,
                                                          Notification.admin_notify==1)
           
            if notification_id and not user.user_type in [1,2]:
                getNotify = getNotify.filter(ArticleHistory.id==notification_id).first()

                if not getNotify:
                    return {"status":0,"msg":"Invalid Notification Id"}
                
                if user.user_type==4:
                    getNotify.chief_editor_notify =2
                if user.user_type==5:
                    getNotify.sub_editor_notify =2
                if user.user_type==8:
                    getNotify.journalist_notify =2
                db.commit()
            
            if notification_id and user.user_type in [1,2]:
                getNotifiy = getNotify.filter(Notification.id==notification_id).first()

                if not getNotifiy:
                    return {"status":0,"msg":"Invalid Notification Id"}
                getNotifiy.admin_notify=2
                getNotifiy.admin_id=user.id
                db.commit()

            if read_type==2:
                update_data = {}

                if user.user_type in [1,2]:
                    getNotify=getNotify.update({"admin_notify":2,
                                                "admin_id":user.id})

                if user.user_type == 4:
                    getNotify=getNotify.filter(
                        ArticleHistory.chief_editor_id == user.id
                    ).update({"chief_editor_notify":2})

                elif user.user_type == 5:
                    getNotify=getNotify.filter(
                        ArticleHistory.sub_editor_id == user.id
                    ).update({"sub_editor_notify":2})

                elif user.user_type == 8:
                    getNotify=getNotify.filter(
                        ArticleHistory.journalist_id == user.id
                    ).update({"journalist_notify":2})

  
                db.commit()

            message ="Success."


            return {"status":1,"msg":"Notification Read"}
        else:
            return {'status':0,"msg":"You are not authenticated to read notification"}
    else:
        return {'status':-1,"msg":"Your login session expires.Please login again."}
    