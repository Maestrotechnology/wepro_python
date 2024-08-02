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
                cast(Article.created_at, Date) == current_date,
                Article.status==1
            )

            articleAction = (
                    db.query(
                        func.sum(case((ArticleHistory.content_status == 1, 1), else_=0)).label("new"),
                        func.sum(case((ArticleHistory.content_status == 2, 1), else_=0)).label("review"),
                        func.sum(case((ArticleHistory.content_status == 3, 1), else_=0)).label("comment"),
                        func.sum(case((ArticleHistory.content_status == 4, 1), else_=0)).label("se_approved"),
                        func.sum(case((ArticleHistory.content_status == 5, 1), else_=0)).label("ce_approved")
                    )
                    .join(
                        Article,ArticleHistory.article_id == Article.id
                    )
                    .filter(
                        Article.status==1,
                        cast(ArticleHistory.created_at, Date) == current_date,
                        ArticleHistory.status == 1,
                ))
            
            
            if user.user_type==4:

                totalArticle=totalArticle.filter(
                Article.chief_editor_id==user.id,
                                               )
                articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)
                
            if user.user_type==5:

                totalArticle=totalArticle.filter(
                Article.sub_editor_id==user.id,
                                               )
                articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)

                
            if user.user_type==8:

                totalArticle=totalArticle.filter(
                Article.created_by==user.id,
                                               )
                articleAction = articleAction.filter(ArticleHistory.journalist_id==user.id)

                
            totalArticle = totalArticle.scalar()
            artcileDet = articleAction.first()
           
            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "total_article": totalArticle,
                "review": artcileDet.review or 0,
                "comment": artcileDet.comment or 0,
                "approved":artcileDet.ce_approved or 0 if user.user_type!=5 else artcileDet.se_approved or 0
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
                        func.sum(case((ArticleHistory.topic_status == 1, 1), else_=0)).label("new"),
                        func.sum(case((ArticleHistory.topic_status == 2, 1), else_=0)).label("review"),
                        func.sum(case((ArticleHistory.topic_status == 3, 1), else_=0)).label("comment"),
                        func.sum(case((ArticleHistory.topic_status == 4, 1), else_=0)).label("se_approved"),
                        func.sum(case((ArticleHistory.topic_status == 5, 1), else_=0)).label("ce_approved")
                    )
                    .join(
                        Article,ArticleHistory.article_id == Article.id
                    )
                    .filter(
                        Article.status==1,
                        cast(ArticleHistory.created_at, Date) == current_date,
                        ArticleHistory.status == 1,
                ))
            
            
            if user.user_type==4:

                totalArticle=totalArticle.filter(
                Article.chief_editor_id==user.id,
                                               )
                
                articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)

                
            if user.user_type==5:

                totalArticle=totalArticle.filter(
                Article.sub_editor_id==user.id,
                                               )
                articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)

                
            if user.user_type==8:

                totalArticle=totalArticle.filter(
                Article.created_by==user.id,
                                               )
                articleAction = articleAction.filter(ArticleHistory.journalist_id==user.id)

                
            totalArticle = totalArticle.scalar()
            artcileDet = articleAction.first()
           
            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "total_article": totalArticle,
                "review": artcileDet.review or 0,
                "comment": artcileDet.comment or 0,
                "approved":artcileDet.ce_approved or 0 if user.user_type!=5 else artcileDet.se_approved or 0
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



# @router.post("/test_topic_barchart")
# async def testTopicBarchart(db:Session=Depends(deps.get_db),
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

#              latest_status_up_to_date = (
#                 db.query(
#                     ArticleHistory.article_id,
#                     func.max(ArticleHistory.created_at).label('latest_created_at')
#                 )
#                 .filter(cast(ArticleHistory.created_at, Date) <= current_date)
#                 .group_by(ArticleHistory.article_id)
#                 .subquery()
#             )

#             # Subquery to get the actual latest status for each article as of the latest_created_at date
#             latest_status_subquery = (
#                 db.query(
#                     ArticleHistory.article_id,
#                     ArticleHistory.topic_status,
#                     ArticleHistory.created_at
#                 )
#                 .join(
#                     latest_status_up_to_date,
#                     and_(
#                         ArticleHistory.article_id == latest_status_up_to_date.c.article_id,
#                         ArticleHistory.created_at == latest_status_up_to_date.c.latest_created_at
#                     )
#                 )
#                 .subquery()
#             )

#             # Subquery to get the status recorded on the current date
#             current_date_status = (
#                 db.query(
#                     ArticleHistory.article_id,
#                     ArticleHistory.topic_status
#                 )
#                 .filter(cast(ArticleHistory.created_at, Date) == current_date)
#                 .subquery()
#             )

#             # Join the current date status with the latest status and filter out the ones that are not the latest
#             status_comparison = (
#                 db.query(
#                     current_date_status.c.topic_status,
#                     func.count().label('count')
#                 )
#                 .outerjoin(
#                     latest_status_subquery,
#                     and_(
#                         current_date_status.c.article_id == latest_status_subquery.c.article_id,
#                         current_date_status.c.topic_status == latest_status_subquery.c.topic_status
#                     )
#                 )
#                 .filter(
#                     or_(
#                         func.coalesce(latest_status_subquery.c.latest_created_at, current_date) == current_date,
#                         latest_status_subquery.c.latest_created_at.is_(None)
#                     )
#                 )
#                 .group_by(current_date_status.c.topic_status)
#             )

#             articleAction = (
#                 db.query(
#                     func.sum(case((status_comparison.c.topic_status == 1, status_comparison.c.count), else_=0)).label("new"),
#                     func.sum(case((status_comparison.c.topic_status == 2, status_comparison.c.count), else_=0)).label("review"),
#                     func.sum(case((status_comparison.c.topic_status == 3, status_comparison.c.count), else_=0)).label("comment"),
#                     func.sum(case((status_comparison.c.topic_status == 4, status_comparison.c.count), else_=0)).label("se_approved"),
#                     func.sum(case((status_comparison.c.topic_status == 5, status_comparison.c.count), else_=0)).label("ce_approved")
#                 )
#             )

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
