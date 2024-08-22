from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.utils import *

router = APIRouter()


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
                    # ArticleHistory.chief_editor_id==user.id,
                                                   ArticleHistory.chief_editor_notify==1)

            if user.user_type ==5:
                getAllNotify = getAllNotify.filter(
                    # ArticleHistory.sub_editor_id==user.id,
                                                   ArticleHistory.sub_editor_notify==1)

            if user.user_type ==8:
                getAllNotify = getAllNotify.filter(ArticleHistory.journalist_id==user.id,
                                                   ArticleHistory.journalist_notify==1)

            totalCount = getAllNotify.count()
            totalPages,offset,limit = get_pagination(totalCount,page,size)
            getAllNotify = getAllNotify.limit(limit).offset(offset).all()

            dataList=[]
            if getAllNotify:
                for row in getAllNotify:
                    dataList.append({
                "article_history_id":row.id,
                "comment":row.comment,
                "history_type":row.history_type,
                "article_status":row.content_status if row.history_type==2 else (row.topic_status if row.history_type==1 else None),
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
           
            if notification_id:
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

            if read_type==2:
                update_data = {}

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
    