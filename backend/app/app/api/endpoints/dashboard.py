from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime,date,timedelta
from app.utils import *
from sqlalchemy import or_,func,case,extract,cast,Date
from app.core import security

import random


router = APIRouter()


import calendar


# @router.post("/pie_chart")
# async def pieChart(db:Session = Depends(deps.get_db),
#                    token:str=Form(...)
#                     ,journalist_id:int=Form(None),
#                     state_id:int=Form(None),
#                     city_id:int=Form(None),
#                     fromDatetime:datetime=Form(None),
#                    todatetime:datetime=Form(None)):
    
#     user = deps.get_user_token(db=db,token=token)
#     if user:
#         today = datetime.now(settings.tz_IN)
#         getMonth =calendar.monthrange(today.year, today.month)[1]
#         if not fromDatetime:
#             fromDatetime = today.replace(day=1,hour=0,minute=0,second=0)
#         else:
#             fromDatetime = fromDatetime.replace(hour=0,minute=0,second=0)
#         if not todatetime:
#             todatetime = today.replace( hour=23,minute=59,second=59)
#         else:
#             todatetime = todatetime.replace(hour=23,minute=59,second=59)

#         getTotalData = (
#             db.query(
#                 func.count(case((Article.status == 1, 1))).label("total"),
#                 func.count(case((Article.content_approved == 1, 1))).label("new"),
#                 func.count(case((Article.content_approved == 0, 1))).label("not_submitted"),
#                 func.count(case((Article.content_approved == 3, 1))).label("published"),
#                 func.count(case((Article.content_approved == 4, 1))).label("on_hold"),
#             ) ).filter(Article.created_at.between(fromDatetime,todatetime),Article.status == 1)
        
#         if journalist_id:
#             getTotalData = getTotalData.filter(Article.created_by == journalist_id )

#         if state_id:
#             getTotalData = getTotalData.filter(Article.state_id == state_id)
#         if city_id:
#             getTotalData = getTotalData.filter(Article.city_id == city_id)
        
#         getTotalData = getTotalData.all()

#         totalData = []  

#         if getTotalData:
#             for total,new,not_submitted,published,on_hold in getTotalData:
#                 totalData=[ {
#                     "label":"Total",
#                     "value":total
#                 },
#                 {
#                     "label":"New",
#                     "value":new
#                 },
#                 {
#                     "label":"Not Submitted",
#                     "value":not_submitted
#                 },
#                 {
#                     "label":"Published",
#                     "value":published
#                 },
#                 {
#                     "label":"On Hold",
#                     "value":on_hold
#                 }
      
#                 ]
#         return {"status":1,"msg":"Success","data":totalData}
#     else:
#         return {"status":-1,"msg":"Sorry your login session expires.Please login again."}

# def get_user_type_stats(db, user_type):
#     return db.query(
#         func.sum(case((User.status == 1, 1), else_=0)).label("total"),
#         func.sum(case((User.is_active == 1, 1), else_=0)).label("active"),
#         func.sum(case((User.is_active == 2, 1), else_=0)).label("inactive"),
#     ).filter(User.status == 1, User.user_type == user_type).first()

# @router.post("/all_user_count")
# async def allDataCount(
#     db: Session = Depends(deps.get_db),
#     token: str = Form(...),
# ):
#     user = deps.get_user_token(db=db, token=token)
#     if user:
#         today = datetime.now(settings.tz_IN)
#         fromdatetime = today.replace(day=1, month=1).strftime("%Y-%m-%d 00:00:00")
#         todatetime = today.replace(day=31, month=12).strftime("%Y-%m-%d 23:59:59")

#         # Query to get total admin users regardless of user_type
#         getUserData = db.query(
#             func.sum(case((User.status == 1, 1), else_=0)).label("total_user"),
#             func.sum(case((User.is_active == 1, 1), else_=0)).label("user_active"),
#             func.sum(case((User.is_active == 2, 1), else_=0)).label("user_inactive"),
#         ).filter(User.status == 1, User.user_type != 1).first()

#         # Query to get statistics for specific user types
#         admin_data = get_user_type_stats(db, 2)  # Admin user type
#         hr_data = get_user_type_stats(db, 3)     # HR user type
#         chief_data = get_user_type_stats(db, 4)  # Chief Editor user type
#         sub_editor_data = get_user_type_stats(db, 5)  # Sub Editor user type
#         dig_str_data = get_user_type_stats(db, 6)  # Digital Strategist user type
#         tl_str_data = get_user_type_stats(db, 7)  # Digital Strategist user type
#         journalist_data = get_user_type_stats(db, 8)  # Journalist user type
#         member_data = get_user_type_stats(db, 9)  # Member user type

#         return {
#             "status": 1,
#             "msg": "Success",
#             "data": {
#                 "total_user": getUserData.total_user or 0,
#                 "user_active": getUserData.user_active or 0,
#                 "user_inactive": getUserData.user_inactive or 0,
#                 "admin": {
#                     "total": admin_data.total or 0,
#                     "active": admin_data.active or 0,
#                     "inactive": admin_data.inactive or 0,
#                 },
#                 "hr": {
#                     "total": hr_data.total or 0,
#                     "active": hr_data.active or 0,
#                     "inactive": hr_data.inactive or 0,
#                 },
#                 "chief_editor": {
#                     "total": chief_data.total or 0,
#                     "active": chief_data.active or 0,
#                     "inactive": chief_data.inactive or 0,
#                 },
#                 "sub_editor": {
#                     "total": sub_editor_data.total or 0,
#                     "active": sub_editor_data.active or 0,
#                     "inactive": sub_editor_data.inactive or 0,
#                 },
#                  "technical_lead": {
#                     "total": dig_str_data.total or 0,
#                     "active": dig_str_data.active or 0,
#                     "inactive": dig_str_data.inactive or 0,
#                 },
#                 "digital_strategist": {
#                     "total": dig_str_data.total or 0,
#                     "active": dig_str_data.active or 0,
#                     "inactive": dig_str_data.inactive or 0,
#                 },
#                 "journalist": {
#                     "total": journalist_data.total or 0,
#                     "active": journalist_data.active or 0,
#                     "inactive": journalist_data.inactive or 0,
#                 },
#                 "member": {
#                     "total": member_data.total or 0,
#                     "active": member_data.active or 0,
#                     "inactive": member_data.inactive or 0,
#                 },
#             },
#         }
#     else:
#         return {"status": -1, "msg": "Your login session expires. Please login again."}
    



@router.post("/article_barchart")
async def articleBarchart(db:Session=Depends(deps.get_db),
                     token:str = Form(...),
                     journalist_id:int=Form(None),
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

            totalArticle = db.query(Article).filter(
                cast(Article.created_at, Date) == current_date,
                Article.status == 1,
            ).count()

            published = db.query(Article).filter(
                cast(Article.published_at, Date) == current_date,
                Article.status == 1,
            ).count()

            # getRejected = db.query(Article).filter(
            #     cast(Article.rejected_at, Date) == current_date,
            #     Article.status == 1,
            # ).count()

            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "total_article": totalArticle,
                "published": published,
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
                "requested": getReq,
                "accepted": getApproved,
                "rejected": getRejected,
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

    #     data = {
    #         "displayName":"Total Users",
    #         "key":"total_counts",
    #         "value":getTotalData.total,
    #         "colorCode":"#328CD1",
    #         "type":1,
    #         "leads":{"displayName":"Users","value":(getTotalData.total - len(getOverDue)) if user.user_type in 1,2 else getTotalData.total},
    #         "over_due":{"displayName":"Over Due","value":len(getOverDue)}if user.user_type in 1,2 else {}},
    #         {
    #         "displayName":"Assigned Users",
    #         "key":"assigned_count",
    #         "value":getTotalData.assigned,
    #         "colorCode":"#2AB95A",
    #         "type":2,
    #         "leads":{"displayName":"Users","value":getTotalData.assigned }},
         
    #     {
    #         "displayName":"Total Quotation",
    #         "key":"quotation_count",
    #         "value":getTotalData.quotation,
    #         "colorCode":"#EB9C04",
    #         "leads":{"displayName":"Users","value":getTotalData.quotation },
            
    #         "type":4
    #     },
    #     {
    #         "displayName":"Total Followup",
    #         "key":"followup_count",
    #         "value":getTotalData.followup,
    #         "colorCode":"#FA5B62",
    #         "type":5,
    #         "leads":{"displayName":"Users","value":getTotalData.followup },
           
    #     },
    #     {
    #         "displayName":"Total Orders",
    #         "key":"orders_count",
    #         "value":getTotalData.orders,
    #         "colorCode":"#F87A05",
    #         "type":6,
    #         "leads":{"displayName":"Users","value":getTotalData.orders },
           
    #     },
    #     {
    #         "displayName":"Missed Users",
    #         "key":"missed_count",
    #         "value":getTotalData.missed,
    #         "colorCode":"#8154FF",
    #         "type":7,
    #         "leads":{"displayName":"Users","value":getTotalData.missed }
    #     }
        
    #     return {"status":1,'msg':"Success.","data":data}
    # else:
    #     return {"status":-1,"msg":"Sorry your login session expires.Please login again."}
