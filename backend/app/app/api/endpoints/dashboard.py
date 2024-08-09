from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from datetime import date,timedelta
from app.utils import *
from sqlalchemy import or_,func,case,extract,cast,Date,distinct,and_

import random


router = APIRouter()


import calendar


# @router.post("/content_barchart")
# async def contentBarchart(db:Session=Depends(deps.get_db),
#                      token:str = Form(...),
#                      fromdate: date = Form(None),
#                       page:int=1,size:int=10,
#                     todate: date = Form(None)):
    
#     user = deps.get_user_token(db=db,token=token)
#     if user:
#         data = []
#         current_date = fromdate
#         offset = (page - 1) * size
#         days = (todate - fromdate).days + 1
#         dates_to_query = [fromdate + timedelta(days=i) for i in range(days)]

#         paginated_dates = dates_to_query[offset:offset + size]

#         for current_date in paginated_dates:
#             next_date = current_date + timedelta(days=1)

#             totalArticle = db.query(func.count(distinct(Article.id))).filter(
#                 cast(Article.created_at, Date) == current_date,
#                 Article.status==1
#             )

#             articleAction = (
#                     db.query(
#                         func.sum(case((ArticleHistory.content_status == 1, 1), else_=0)).label("new"),
#                         func.sum(case((ArticleHistory.content_status == 2, 1), else_=0)).label("review"),
#                         func.sum(case((ArticleHistory.content_status == 3, 1), else_=0)).label("comment"),
#                         func.sum(case((ArticleHistory.content_status == 4, 1), else_=0)).label("se_approved"),
#                         func.sum(case((ArticleHistory.content_status == 5, 1), else_=0)).label("ce_approved")
#                     )
#                     .join(
#                         Article,ArticleHistory.article_id == Article.id
#                     )
#                     .filter(
#                         Article.status==1,
#                         cast(ArticleHistory.created_at, Date) == current_date,
#                         ArticleHistory.status == 1,
#                 ))
            
            
#             if user.user_type==4:

#                 totalArticle=totalArticle.filter(
#                 Article.chief_editor_id==user.id,
#                                                )
#                 articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)
                
#             if user.user_type==5:

#                 totalArticle=totalArticle.filter(
#                 Article.sub_editor_id==user.id,
#                                                )
#                 articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)

                
#             if user.user_type==8:

#                 totalArticle=totalArticle.filter(
#                 Article.created_by==user.id,
#                                                )
#                 articleAction = articleAction.filter(ArticleHistory.journalist_id==user.id)

                
#             totalArticle = totalArticle.scalar()
#             artcileDet = articleAction.first()
           
#             data.append({
#                 "date": current_date.strftime("%Y-%m-%d"),
#                 "total_article": totalArticle,
#                 "review": artcileDet.review or 0,
#                 "comment": artcileDet.comment or 0,
#                 "approved":artcileDet.ce_approved or 0 if user.user_type!=5 else artcileDet.se_approved or 0
#                 # "rejected": getRejected,
#             })

#         total_pages = (days + size - 1) // size  # Calculate total pages

#         return {
#             "status": 1,
#             "msg": "Success",
#             "data": {
#                 "page": page,
#                 "size": size,
#                 "total_pages": total_pages,
#                 "total_count": days,
#                 "items": data,
#             }
#         }
#     else:
#         return {"status": -1, "msg": "Sorry, your login session has expired. Please login again."}



# @router.post("/topic_barchart")
# async def topicBarchart(db:Session=Depends(deps.get_db),
#                      token:str = Form(...),
#                      fromdate: date = Form(None),
#                       page:int=1,size:int=10,
#                     todate: date = Form(None)):
    
#     user = deps.get_user_token(db=db,token=token)
#     if user:
#         data = []
#         current_date = fromdate
#         offset = (page - 1) * size
#         days = (todate - fromdate).days + 1
#         dates_to_query = [fromdate + timedelta(days=i) for i in range(days)]

#         paginated_dates = dates_to_query[offset:offset + size]

#         for current_date in paginated_dates:
#             next_date = current_date + timedelta(days=1)

#             totalArticle = db.query(func.count(distinct(Article.id))).filter(
#                 cast(Article.created_at, Date) == current_date,
#                 Article.status==1
#             )

#             articleAction = (
#                     db.query(
#                         func.sum(case((ArticleHistory.topic_status == 1, 1), else_=0)).label("new"),
#                         func.sum(case((ArticleHistory.topic_status == 2, 1), else_=0)).label("review"),
#                         func.sum(case((ArticleHistory.topic_status == 3, 1), else_=0)).label("comment"),
#                         func.sum(case((ArticleHistory.topic_status == 4, 1), else_=0)).label("se_approved"),
#                         func.sum(case((ArticleHistory.topic_status == 5, 1), else_=0)).label("ce_approved")
#                     )
#                     .join(
#                         Article,ArticleHistory.article_id == Article.id
#                     )
#                     .filter(
#                         Article.status==1,
#                         cast(ArticleHistory.created_at, Date) == current_date,
#                         ArticleHistory.status == 1,
#                 ))
            
            
#             if user.user_type==4:

#                 totalArticle=totalArticle.filter(
#                 Article.chief_editor_id==user.id,
#                                                )
                
#                 articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)

                
#             if user.user_type==5:

#                 totalArticle=totalArticle.filter(
#                 Article.sub_editor_id==user.id,
#                                                )
#                 articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)

                
#             if user.user_type==8:

#                 totalArticle=totalArticle.filter(
#                 Article.created_by==user.id,
#                                                )
#                 articleAction = articleAction.filter(ArticleHistory.journalist_id==user.id)

                
#             totalArticle = totalArticle.scalar()
#             artcileDet = articleAction.first()
           
#             data.append({
#                 "date": current_date.strftime("%Y-%m-%d"),
#                 "total_article": totalArticle,
#                 "review": artcileDet.review or 0,
#                 "comment": artcileDet.comment or 0,
#                 "approved":artcileDet.ce_approved or 0 if user.user_type!=5 else artcileDet.se_approved or 0
#                 # "rejected": getRejected,
#             })

#         total_pages = (days + size - 1) // size  # Calculate total pages

#         return {
#             "status": 1,
#             "msg": "Success",
#             "data": {
#                 "page": page,
#                 "size": size,
#                 "total_pages": total_pages,
#                 "total_count": days,
#                 "items": data,
#             }
#         }
#     else:
#         return {"status": -1, "msg": "Sorry, your login session has expired. Please login again."}

    
@router.post("/journalist_barchart")
async def journalistbarchart(
    db: Session = Depends(deps.get_db),
    token: str = Form(None),
    fromdate: date = Form(None),
    todate: date = Form(None),
   page:int=1,size:int=10):
    
    user = deps.get_user_token(db=db, token=token)
    if user:
        data = []
        current_date = fromdate
        offset = (page - 1) * size
        days = (todate - fromdate).days + 1
        dates_to_query = [fromdate + timedelta(days=i) for i in range(days)]

        paginated_dates = dates_to_query[offset:offset + size]

        for current_date in paginated_dates:
            next_date = current_date + timedelta(days=1)

            getReq = db.query(User).filter(
                cast(User.requested_at, Date) == current_date,
                User.status == 1,
                User.user_type == 8
            ).count()

            getApproved = db.query(User).filter(
                cast(User.approved_at, Date) == current_date,
                User.status == 1,
                User.user_type == 8
            ).count()

            getRejected = db.query(User).filter(
                cast(User.rejected_at, Date) == current_date,
                User.status == 1,
                User.user_type == 8
            ).count()

            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "requested": getReq or 0,
                "accepted": getApproved or 0,
                "rejected": getRejected or 0,
            })

        total_pages = (days + size - 1) // size  # Calculate total pages

        return {
            "status": 1,
            "msg": "Success",
            "data": {
                "page": page,
                "size": size,
                "total_pages": total_pages,
                "total_count": days,
                "items": data,
            }
        }
    else:
        return {"status": -1, "msg": "Sorry, your login session has expired. Please login again."}


@router.post("/topic_barchart")
async def topicBarchart(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     fromdate: date = Form(None),
                      page:int=1,size:int=10,
                    todate: date = Form(None)):
    
    user = deps.get_user_token(db=db,token=token)
    if user:
        data = []
        current_date = fromdate
        offset = (page - 1) * size
        days = (todate - fromdate).days + 1
        dates_to_query = [fromdate + timedelta(days=i) for i in range(days)]

        paginated_dates = dates_to_query[offset:offset + size]

        for current_date in paginated_dates:
            next_date = current_date + timedelta(days=1)

            totalArticle = db.query(func.count(distinct(Article.id))).filter(
                cast(Article.created_at, Date) == current_date,
                Article.status==1
            )

            articleAction = (
                    db.query(
                        # func.sum(case((Article.content_status == 1, 1), else_=0)).label("new"),
                        func.sum(case((cast(Article.topic_ce_review_at, Date) == current_date, 1), else_=0)).label("review"),
                        func.sum(case((cast(Article.topic_ce_cmnt_at, Date) == current_date, 1), else_=0)).label("comment"),
                        func.sum(case((cast(Article.topic_ce_approved_at, Date) == current_date, 1), else_=0)).label("approved")
                    )
                    .filter(
                        Article.status==1,
                ))
            
            
            if user.user_type==4:

                totalArticle=totalArticle.filter(
                Article.chief_editor_id==user.id,
                                               )
                
                articleAction = articleAction.filter(Article.chief_editor_id==user.id)

                
            if user.user_type==5:


                articleAction = (
                    db.query(
                        # func.sum(case((Article.content_status == 1, 1), else_=0)).label("new"),
                        func.sum(case((cast(Article.topic_se_review_at, Date) == current_date, 1), else_=0)).label("review"),
                        func.sum(case((cast(Article.topic_se_cmnt_at, Date) == current_date, 1), else_=0)).label("comment"),
                        func.sum(case((cast(Article.topic_se_approved_at, Date) == current_date, 1), else_=0)).label("approved")
                    )
                    .filter(
                        Article.status==1,
                ))

                totalArticle=totalArticle.filter(
                Article.sub_editor_id==user.id,
                                               )
                articleAction = articleAction.filter(Article.chief_editor_id==user.id)

                
            if user.user_type==8:
                

                totalArticle=totalArticle.filter(
                Article.created_by==user.id,
                                               )
                articleAction = articleAction.filter(Article.created_by==user.id)

                
            totalArticle = totalArticle.scalar()
            artcileDet = articleAction.first()
           
            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "total_article": totalArticle,
                "review": artcileDet.review or 0 if artcileDet else 0,
                "comment": artcileDet.comment or 0 if artcileDet else 0,
                "approved":artcileDet.approved or  0 if artcileDet else 0
                # "rejected": getRejected,
            })

        total_pages = (days + size - 1) // size  # Calculate total pages

        return {
            "status": 1,
            "msg": "Success",
            "data": {
                "page": page,
                "size": size,
                "total_pages": total_pages,
                "total_count": days,
                "items": data,
            }
        }
    else:
        return {"status": -1, "msg": "Sorry, your login session has expired. Please login again."}

@router.post("/content_barchart")
async def contentBarchart(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     fromdate: date = Form(None),
                      page:int=1,size:int=10,
                    todate: date = Form(None)):
    
    user = deps.get_user_token(db=db,token=token)
    if user:
        data = []
        current_date = fromdate
        offset = (page - 1) * size
        days = (todate - fromdate).days + 1
        dates_to_query = [fromdate + timedelta(days=i) for i in range(days)]

        paginated_dates = dates_to_query[offset:offset + size]

        for current_date in paginated_dates:
            next_date = current_date + timedelta(days=1)

            totalArticle = db.query(func.count(distinct(Article.id))).filter(
                cast(Article.content_created_at, Date) == current_date,
                Article.status==1
            )

            articleAction = (
                    db.query(
                        # func.sum(case((Article.content_status == 1, 1), else_=0)).label("new"),
                        func.sum(case((cast(Article.content_ce_review_at, Date) == current_date, 1), else_=0)).label("review"),
                        func.sum(case((cast(Article.content_ce_cmnt_at, Date) == current_date, 1), else_=0)).label("comment"),
                        func.sum(case((cast(Article.published_at, Date) == current_date, 1), else_=0)).label("approved")
                    )
                    .filter(
                        Article.status==1,
                ))
            
            if user.user_type==4:

                totalArticle=totalArticle.filter(
                Article.chief_editor_id==user.id,
                                               )
                articleAction = articleAction.filter(Article.chief_editor_id==user.id)
                
            if user.user_type==5:

                articleAction = (
                    db.query(
                        # func.sum(case((Article.content_status == 1, 1), else_=0)).label("new"),
                        func.sum(case((cast(Article.content_se_review_at, Date) == current_date, 1), else_=0)).label("review"),
                        func.sum(case((cast(Article.content_se_cmnt_at, Date) == current_date, 1), else_=0)).label("comment"),
                        func.sum(case((cast(Article.content_se_approved_at, Date) == current_date, 1), else_=0)).label("approved")
                    )
                    .filter(
                        Article.status==1,
                ))
            

                totalArticle=totalArticle.filter(
                Article.sub_editor_id==user.id,
                                               )
                articleAction = articleAction.filter(Article.chief_editor_id==user.id)

                
            if user.user_type==8:

                totalArticle=totalArticle.filter(
                Article.created_by==user.id,
                                               )
                articleAction = articleAction.filter(Article.created_by==user.id)

                
            totalArticle = totalArticle.scalar()
            artcileDet = articleAction.first()
           
            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "total_article": totalArticle,
                "review": artcileDet.review or 0 if artcileDet else 0,
                "comment": artcileDet.comment or 0 if artcileDet else 0,
                "approved":artcileDet.approved or  0 if artcileDet else 0
                # "rejected": getRejected,
            })

        total_pages = (days + size - 1) // size  # Calculate total pages

        return {
            "status": 1,
            "msg": "Success",
            "data": {
                "page": page,
                "size": size,
                "total_pages": total_pages,
                "total_count": days,
                "items": data,
            }
        }
    else:
        return {"status": -1, "msg": "Sorry, your login session has expired. Please login again."}