from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session,aliased
from app.models import *
from app.api import deps
from datetime import date,timedelta
from app.utils import *
from sqlalchemy import or_,func,case,extract,cast,Date,distinct,and_
from typing import Optional
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

@router.post("/categorywise_barchart")
async def categorywise_barchart(
    db: Session = Depends(deps.get_db),
    token: str = Form(None),
   page:int=1,size:int=10):
    
    user = deps.get_user_token(db=db, token=token)
    if user:
        # getAllArticle = (
        #     db.query(
        #         Category.title,
        #         func.count(Article.id).label("article_count")  # Count of articles
        #     )
        #     .outerjoin(Article, Category.id == Article.category_id)  # Outer join to include all categories
        #     .filter(
        #         Article.status == 1, 
        #         Article.content_approved == 5,
        #         Article.created_by == user.id
        #     )
        #     .group_by(Category.id)  # Group by Category ID to get the count for each category
        # )
        userCreationDt = user.created_at

        article_count_subquery = db.query(
            Article.category_id,
            func.count(Article.id).label('article_count')
        ).filter(
            Article.status == 1,
            Article.content_approved == 4,
        )

        if user.user_type in [4,5]:
            article_count_subquery=article_count_subquery.filter(Article.created_at>=userCreationDt)


        if user.user_type==8:
            article_count_subquery =article_count_subquery.filter(Article.created_by == user.id)

        article_count_subquery = article_count_subquery.group_by(Article.category_id).subquery()

        # Main query to get categories and join with the article count subquery
        getAllArticle = db.query(
            Category.title,
            func.coalesce(article_count_subquery.c.article_count, 0).label('article_count'),
            case(
                [(func.coalesce(article_count_subquery.c.article_count, 0) > 0, 'Yes')],
                else_='No'
            ).label('has_articles')
        ).outerjoin(
            article_count_subquery, Category.id == article_count_subquery.c.category_id
        ).filter(Category.status==1).order_by(Category.sort_order.asc())

        totalCount = getAllArticle.count()
        
        totalPages,offset,limit = get_pagination(totalCount,page,size)
        getAllArticle = getAllArticle.limit(limit).offset(offset).all()
        dataList = []
        for row in getAllArticle:
          
            dataList.append({"category_name":row.title ,
                             "article_count":row.article_count})


        data=({"page":page,"size":size,
            "total_page":totalPages,
            "total_count":totalCount,
            "items":dataList})
        return ({"status":1,"msg":"Success","data":data})
    else:
        return ({"status": -1,"msg": "Sorry your login session expires.Please login again."})
    
 
@router.post("/journalist_chart")
async def journalistChart(
    db: Session = Depends(deps.get_db),
    token: str = Form(None),
):
    
    user = deps.get_user_token(db=db, token=token)
    if user:
        totalUser =db.query(func.count(User.id)).filter(User.status==1,User.user_type==8).scalar() or 0
        userCount = db.query(
                    # func.sum(case((Article.content_status == 1, 1), else_=0)).label("new"),
                   func.sum(case([(User.request_user==1,1)],else_=0)).label("requested"),
                   func.sum(case([(User.is_request==2,1)],else_=0)).label("accepted"),
                   func.sum(case([(User.is_request==-1,1)],else_=0)).label("rejected")).\
                    filter(User.status==1,User.user_type==8).first()
        data={
            "total_journalist": totalUser,
            "requested": userCount.requested or 0 if userCount else 0,
            "accepted": userCount.accepted or 0 if userCount else 0,
            "rejected":userCount.rejected or  0 if userCount else 0
        }
            
        return {
                "status": 1,
                "msg": "Success",
                "data":data
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
    
@router.post("/topic_barchart")
async def topicBarchart(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                    ):
    
    user = deps.get_user_token(db=db,token=token)
    if user:
       

        totalArticle = db.query(func.count(distinct(Article.id))).filter(
            Article.status==1,Article.save_for_later==0,Article.topic_se_approved!=None)
        completedArticle = db.query(func.count(distinct(Article.id))).filter(
            Article.status==1,Article.save_for_later==0,Article.topic_approved==4,Article.topic_se_approved!=None)

        # articleAction = db.query(
        #             # func.sum(case((Article.content_status == 1, 1), else_=0)).label("new"),
        #            func.sum(case([(ArticleHistory.topic_status==2,1)],else_=0)).label("review"),
        #            func.sum(case([(ArticleHistory.topic_status==3,1)],else_=0)).label("comment"),
        #            func.sum(case([(ArticleHistory.topic_status==4,1)],else_=0)).label("approved")).join(
        #                Article,ArticleHistory.article_id==Article.id).filter(Article.status==1,
        #                                                                      Article.topic_se_approved!=None,
        #                                                                      Article.save_for_later==0)

     
        subquery = db.query(
                Article.id,
                ArticleHistory.topic_status
            ).join(
                ArticleHistory, ArticleHistory.article_id == Article.id
            ).filter(
                Article.status == 1,
                Article.topic_se_approved != None,
                Article.save_for_later == 0
            ).distinct(Article.id).subquery()

            # Main query to aggregate counts based on distinct articles
        articleAction = db.query(
            func.sum(case([(subquery.c.topic_status == 2, 1)], else_=0)).label("review"),
            func.sum(case([(subquery.c.topic_status == 3, 1)], else_=0)).label("comment"),
            func.sum(case([(subquery.c.topic_status == 4, 1)], else_=0)).label("approved")
        )
                    
        completedArticle = completedArticle.scalar()
        totalArticle = totalArticle.scalar()
        artcileDet = articleAction.first()
            
        data={
                    "total_article": totalArticle,
                    "review": artcileDet.review or 0 if artcileDet else 0,
                    "comment": artcileDet.comment or 0 if artcileDet else 0,
                    "approved":completedArticle
                    # "approved":artcileDet.approved or  0 if artcileDet else 0
                }
            
        return {
                "status": 1,
                "msg": "Success",
                "data":data
            }
       
    else:
        return {"status": -1, "msg": "Sorry, your login session has expired. Please login again."}

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
#                         # func.sum(case((Article.content_status == 1, 1), else_=0)).label("new"),
#                         func.sum(case((cast(Article.topic_ce_review_at, Date) == current_date, 1), else_=0)).label("review"),
#                         func.sum(case((cast(Article.topic_ce_cmnt_at, Date) == current_date, 1), else_=0)).label("comment"),
#                         func.sum(case((cast(Article.topic_ce_approved_at, Date) == current_date, 1), else_=0)).label("approved")
#                     )
#                     .filter(
#                         Article.status==1,
#                 ))
            
            
#             if user.user_type==4:

#                 # totalArticle=totalArticle.filter(
#                 # Article.chief_editor_id==user.id,
#                 #                                )
                
#                 articleAction = articleAction.filter(Article.chief_editor_id==user.id)

                
#             if user.user_type==5:


#                 articleAction = (
#                     db.query(
#                         # func.sum(case((Article.content_status == 1, 1), else_=0)).label("new"),
#                         func.sum(case((cast(Article.topic_se_review_at, Date) == current_date, 1), else_=0)).label("review"),
#                         func.sum(case((cast(Article.topic_se_cmnt_at, Date) == current_date, 1), else_=0)).label("comment"),
#                         func.sum(case((cast(Article.topic_se_approved_at, Date) == current_date, 1), else_=0)).label("approved")
#                     )
#                     .filter(
#                         Article.status==1,
#                 ))

#                 # totalArticle=totalArticle.filter(
#                 # Article.sub_editor_id==user.id,
#                 #                                )
#                 articleAction = articleAction.filter(Article.sub_editor_id==user.id)

                
#             if user.user_type==8:
#                 articleAction = (
#                     db.query(
#                         func.sum(
#                             case(
                                
#                                     (cast(Article.topic_ce_review_at, Date) == current_date, 1),
#                                     (cast(Article.topic_se_review_at, Date) == current_date, 1)
#                                 ,
#                                 else_=0
#                             )
#                         ).label("review"),
#                         func.sum(
#                             case(
                                
#                                     (cast(Article.topic_ce_cmnt_at, Date) == current_date, 1),
#                                     (cast(Article.topic_se_cmnt_at, Date) == current_date, 1)
#                                 ,
#                                 else_=0
#                             )
#                         ).label("comment"),
#                         func.sum(
#                             case(
#                                 (cast(Article.topic_ce_approved_at, Date) == current_date, 1),
#                                     (cast(Article.topic_se_approved_at, Date) == current_date, 1)
#                                 ,
#                                 else_=0
#                             )
#                         ).label("approved")
#                     )
#                     .filter(Article.status == 1)
#                 )
                

#                 totalArticle=totalArticle.filter(
#                 Article.created_by==user.id,
#                                                )
#                 articleAction = articleAction.filter(Article.created_by==user.id)

                
#             totalArticle = totalArticle.scalar()
#             artcileDet = articleAction.first()
           
#             data.append({
#                 "date": current_date.strftime("%Y-%m-%d"),
#                 "total_article": totalArticle,
#                 "review": artcileDet.review or 0 if artcileDet else 0,
#                 "comment": artcileDet.comment or 0 if artcileDet else 0,
#                 "approved":artcileDet.approved or  0 if artcileDet else 0
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

@router.post("/content_barchart")
async def contentBarchart(
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
):
    user = deps.get_user_token(db=db, token=token)
    
    if user:
        userCreationDt = user.created_at

        # Base queries
        totalArticle = db.query(func.count(distinct(Article.id))).filter(
            Article.status == 1,
            Article.topic_approved == 4,
        )
        
        completedArticle = db.query(func.count(distinct(Article.id))).filter(
            Article.status == 1,
            Article.save_for_later == 0,
        )
        
        # Aliased ArticleHistory
        ArticleHistoryAlias = aliased(ArticleHistory)
        
        # Subquery for distinct articles and their content statuses
        subqueryHistory = db.query(
            Article.id.label('article_id'),
            ArticleHistoryAlias.content_status
        ).join(
            ArticleHistoryAlias, ArticleHistoryAlias.article_id == Article.id
        ).filter(
            Article.status == 1,
            Article.topic_approved == 4,
            Article.save_for_later == 0
        ).distinct(Article.id)

        if user.user_type==4:
            
            
                                                    #   
            totalArticle = totalArticle.filter(Article.save_for_later == 0,
                                               Article.created_at>=userCreationDt,
                                               Article.content_approved.isnot(None))
            subqueryHistory = subqueryHistory.filter( ArticleHistoryAlias.chief_editor_id == user.id,
                ArticleHistoryAlias.is_editor == 2)
            
            completedArticle = completedArticle.filter(
                Article.chief_editor_id == user.id,
            Article.content_approved == 4

            )
            

        if user.user_type==5:
            totalArticle = totalArticle.filter(Article.save_for_later == 0,
                                               Article.created_at>=userCreationDt,
                                               Article.content_se_approved.isnot(None))

            subqueryHistory = subqueryHistory.filter( ArticleHistoryAlias.sub_editor_id == user.id,
                ArticleHistoryAlias.is_editor == 2)
            
            completedArticle = completedArticle.filter(
                Article.sub_editor_id == user.id,
                Article.content_se_approved == 4

            )

        if user.user_type == 8:
        
            subqueryHistory = subqueryHistory.filter( Article.created_by == user.id)
            totalArticle = totalArticle.filter(Article.created_by == user.id)
            completedArticle = completedArticle.filter(
            Article.content_approved == 4,
                Article.created_by == user.id,
            )



            
        subqueryHistory=subqueryHistory.subquery()
        
        # Main query to aggregate counts based on distinct articles
        articleAction = db.query(
            func.sum(case([(subqueryHistory.c.content_status == 2, 1)], else_=0)).label("review"),
            func.sum(case([(subqueryHistory.c.content_status == 3, 1)], else_=0)).label("comment"),
            func.sum(case([(subqueryHistory.c.content_status == 4, 1)], else_=0)).label("approved")
        ).select_from(subqueryHistory)
        
        
        
        if user.user_type in [1, 2,6,7]:
            completedArticle = completedArticle.filter(
                Article.content_approved == 4
            )
        
        # Execute queries
        totalArticle_count = totalArticle.scalar()
        completedArticle_count = completedArticle.scalar()
        articleAction_result = articleAction.first()
        
        # Prepare response data
        data = {
            "total_article": totalArticle_count,
            "review": articleAction_result.review or 0 if articleAction_result else 0,
            "comment": articleAction_result.comment or 0 if articleAction_result else 0,
            "approved": completedArticle_count
        }
        
        return {
            "status": 1,
            "msg": "Success",
            "data": data
        }
    
    else:
        return {"status": -1, "msg": "Sorry, your login session has expired. Please login again."}

