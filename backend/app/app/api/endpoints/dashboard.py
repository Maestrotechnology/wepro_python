from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime,date,timedelta
from app.utils import *
from sqlalchemy import or_,func,case,extract
from app.core import security

import random


router = APIRouter()


import calendar
    
@router.post("/pie_chart")
async def pieChart(db:Session = Depends(deps.get_db),
                   token:str=Form(...)
                    ,journalist_id:int=Form(None),
                    state_id:int=Form(None),
                    city_id:int=Form(None),
                    fromDatetime:datetime=Form(None),
                   todatetime:datetime=Form(None)):
    
    user = deps.get_user_token(db=db,token=token)
    if user:
        today = datetime.now(settings.tz_IN)
        getMonth =calendar.monthrange(today.year, today.month)[1]
        if not fromDatetime:
            fromDatetime = today.replace(day=1,hour=0,minute=0,second=0)
        else:
            fromDatetime = fromDatetime.replace(hour=0,minute=0,second=0)
        if not todatetime:
            todatetime = today.replace( hour=23,minute=59,second=59)
        else:
            todatetime = todatetime.replace(hour=23,minute=59,second=59)

        getTotalData = (
            db.query(
                func.count(case((Article.status == 1, 1))).label("total"),
                func.count(case((Article.content_approved == 1, 1))).label("new"),
                func.count(case((Article.content_approved == 0, 1))).label("not_submitted"),
                func.count(case((Article.content_approved == 3, 1))).label("published"),
                func.count(case((Article.content_approved == 4, 1))).label("on_hold"),
            ) ).filter(Article.created_at.between(fromDatetime,todatetime),Article.status == 1)
        
        if journalist_id:
            getTotalData = getTotalData.filter(Article.created_by == journalist_id )

        if state_id:
            getTotalData = getTotalData.filter(Article.state_id == state_id)
        if city_id:
            getTotalData = getTotalData.filter(Article.city_id == city_id)
        
        getTotalData = getTotalData.all()

        totalData = []  

        if getTotalData:
            for total,new,not_submitted,published,on_hold in getTotalData:
                totalData=[ {
                    "label":"Total",
                    "value":total
                },
                {
                    "label":"New",
                    "value":new
                },
                {
                    "label":"Not Submitted",
                    "value":not_submitted
                },
                {
                    "label":"Published",
                    "value":published
                },
                {
                    "label":"On Hold",
                    "value":on_hold
                }
      
                ]
        return {"status":1,"msg":"Success","data":totalData}
    else:
        return {"status":-1,"msg":"Sorry your login session expires.Please login again."}

def get_user_type_stats(db, user_type):
    return db.query(
        func.sum(case((User.status == 1, 1), else_=0)).label("total"),
        func.sum(case((User.is_active == 1, 1), else_=0)).label("active"),
        func.sum(case((User.is_active == 2, 1), else_=0)).label("inactive"),
    ).filter(User.status == 1, User.user_type == user_type).first()

@router.post("/all_user_count")
async def allDataCount(
    db: Session = Depends(deps.get_db),
    token: str = Form(...),
):
    user = deps.get_user_token(db=db, token=token)
    if user:
        today = datetime.now(settings.tz_IN)
        fromdatetime = today.replace(day=1, month=1).strftime("%Y-%m-%d 00:00:00")
        todatetime = today.replace(day=31, month=12).strftime("%Y-%m-%d 23:59:59")

        # Query to get total admin users regardless of user_type
        getUserData = db.query(
            func.sum(case((User.status == 1, 1), else_=0)).label("total_user"),
            func.sum(case((User.is_active == 1, 1), else_=0)).label("user_active"),
            func.sum(case((User.is_active == 2, 1), else_=0)).label("user_inactive"),
        ).filter(User.status == 1, User.user_type != 1).first()

        # Query to get statistics for specific user types
        admin_data = get_user_type_stats(db, 2)  # Admin user type
        hr_data = get_user_type_stats(db, 3)     # HR user type
        chief_data = get_user_type_stats(db, 4)  # Chief Editor user type
        sub_editor_data = get_user_type_stats(db, 5)  # Sub Editor user type
        dig_str_data = get_user_type_stats(db, 6)  # Digital Strategist user type
        tl_str_data = get_user_type_stats(db, 7)  # Digital Strategist user type
        journalist_data = get_user_type_stats(db, 8)  # Journalist user type
        member_data = get_user_type_stats(db, 9)  # Member user type

        return {
            "status": 1,
            "msg": "Success",
            "data": {
                "total_user": getUserData.total_user or 0,
                "user_active": getUserData.user_active or 0,
                "user_inactive": getUserData.user_inactive or 0,
                "admin": {
                    "total": admin_data.total or 0,
                    "active": admin_data.active or 0,
                    "inactive": admin_data.inactive or 0,
                },
                "hr": {
                    "total": hr_data.total or 0,
                    "active": hr_data.active or 0,
                    "inactive": hr_data.inactive or 0,
                },
                "chief_editor": {
                    "total": chief_data.total or 0,
                    "active": chief_data.active or 0,
                    "inactive": chief_data.inactive or 0,
                },
                "sub_editor": {
                    "total": sub_editor_data.total or 0,
                    "active": sub_editor_data.active or 0,
                    "inactive": sub_editor_data.inactive or 0,
                },
                 "technical_lead": {
                    "total": dig_str_data.total or 0,
                    "active": dig_str_data.active or 0,
                    "inactive": dig_str_data.inactive or 0,
                },
                "digital_strategist": {
                    "total": dig_str_data.total or 0,
                    "active": dig_str_data.active or 0,
                    "inactive": dig_str_data.inactive or 0,
                },
                "journalist": {
                    "total": journalist_data.total or 0,
                    "active": journalist_data.active or 0,
                    "inactive": journalist_data.inactive or 0,
                },
                "member": {
                    "total": member_data.total or 0,
                    "active": member_data.active or 0,
                    "inactive": member_data.inactive or 0,
                },
            },
        }
    else:
        return {"status": -1, "msg": "Your login session expires. Please login again."}
    


@router.post("/new_journalist_monthwise_count")
async def newJournalistPiechart(db:Session = Depends(deps.get_db),
                        token:str = Form(...),
                        year:int=Form(None)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        today = datetime.now(settings.tz_IN)


        data=[]

        today = datetime.now(settings.tz_IN)

        month=today.month

        yearFind=today.year

        if year:
            yearFind = year

        if yearFind!=today.year:
            month = 12
        
        toDatetime = today.replace(year=yearFind,month=month,hour=23,minute=59,second=59)

        fromDateTime = today.replace(year=yearFind,day=1,month=1,hour=0,minute=0,second=0)
        
        getAllUserCount = db.query(  
             extract('month',User.created_at).label('month'),
             func.sum(case((User.status == 1, 1), else_=0)).label("total"),
                                       ).filter(User.status==1,User.user_type==8,User.created_at.between(fromDateTime,toDatetime))
        

        getAllUserCount = getAllUserCount.group_by(extract('month',User.created_at)).all()
        
        result_by_month={}
        formatted_result =[]
      
        if getAllUserCount:
            for month,total in getAllUserCount:

                if month not in result_by_month:
                    result_by_month[month] = {"total": 0}
                        
                result_by_month[month]["total"] = total
        
        endMonth = int(toDatetime.month ) + 1 #to get up to current month data
        fromMonth = int(fromDateTime.month)
        if toDatetime.year != fromDateTime.year:
            if int(toDatetime.year) - int(fromDateTime.year) ==1:
                if int(toDatetime.month ) < int(fromDateTime.month):
                    fromMonth = fromDateTime.month
                    endMonth =13
                    formatted_result = getFormattedData(fromMonth,endMonth,result_by_month,formatted_result)

                    fromMonth = 1
                    endMonth = int(toDatetime.month ) +1
                    formatted_result = getFormattedData(fromMonth,endMonth,result_by_month,formatted_result)
                else:
                    fromMonth=1
                    endMonth =13
                    formatted_result = getFormattedData(fromMonth,endMonth,result_by_month,formatted_result)
            else:
                fromMonth = 1
                endMonth =13
                formatted_result = getFormattedData(fromMonth,endMonth,result_by_month,formatted_result)
        else:
         
            formatted_result = getFormattedData(fromMonth,endMonth,result_by_month,formatted_result)

        return {"status":1,"msg":"Success","data":formatted_result}
    else:
        return {"status":-1,"msg":"Sorry your login session expires.Please login again."}


def getFormattedData(fromMonth,endMonth,result_by_month,formatted_result):
    for month in range(fromMonth,endMonth): # 12 Month
        if month in result_by_month:
            data = result_by_month[month]
            total  = data["total"]
        else:
            total = 0
        import calendar
        # totalCount = open + assigned + demo +  quotation + follow_up + close + order
        formatted_result.append({
                "month": calendar.month_name[month],
                "Total":total
                })
        
    return formatted_result

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
