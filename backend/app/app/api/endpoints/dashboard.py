from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime,date,timedelta
from app.utils import *
from sqlalchemy import or_,func,case
from app.core import security

import random


router = APIRouter()
@router.post("/all_user_count")
async def allDataCount (db:Session = Depends(deps.get_db),
                        token:str=Form(...)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        today = datetime.now(settings.tz_IN)
       
        fromdatetime = today.replace(day=1,month=1).strftime("%Y-%m-%d 00:00:00")
        
        todatetime = today.replace(day=31,month=12).strftime("%Y-%m-%d 23:59:59")        


        getTotalData = (
            db.query(
                func.count(case([(User.status == 1, 1)], else_=0)).label("total"),
                func.count(case([(User.user_type == 2, 1)], else_=0)).label("admin"),
                func.count(case([(User.user_type == 2) & (User.is_active == 1), 1], else_=0)).label("admin_active"),
                func.count(case([(User.user_type == 2) & (User.is_active == 0), 1], else_=0)).label("admin_inactive"),
                func.count(case([(User.user_type == 3, 1)], else_=0)).label("hr"),
                func.count(case([(User.user_type == 3) & (User.is_active == 1), 1], else_=0)).label("hr_active"),
                func.count(case([(User.user_type == 3) & (User.is_active == 0), 1], else_=0)).label("hr_inactive"),
                func.count(case([(User.user_type == 4, 1)], else_=0)).label("chiefEditor"),
                func.count(case([(User.user_type == 4) & (User.is_active == 1), 1], else_=0)).label("chiefEditor_active"),
                func.count(case([(User.user_type == 4) & (User.is_active == 0), 1], else_=0)).label("chiefEditor_inactive"),
                func.count(case([(User.user_type == 5, 1)], else_=0)).label("subEditor"),
                func.count(case([(User.user_type == 5) & (User.is_active == 1), 1], else_=0)).label("subEditor_active"),
                func.count(case([(User.user_type == 5) & (User.is_active == 0), 1], else_=0)).label("subEditor_inactive"),
                func.count(case([(User.user_type == 6, 1)], else_=0)).label("digitalSt"),
                func.count(case([(User.user_type == 6) & (User.is_active == 1), 1], else_=0)).label("digitalSt_active"),
                func.count(case([(User.user_type == 6) & (User.is_active == 0), 1], else_=0)).label("digitalSt_inactive"),
                func.count(case([(User.user_type == 7, 1)], else_=0)).label("journalist"),
                func.count(case([(User.user_type == 7) & (User.is_active == 1), 1], else_=0)).label("journalist_active"),
                func.count(case([(User.user_type == 7) & (User.is_active == 0), 1], else_=0)).label("journalist_inactive"),
                func.count(case([(User.user_type == 8, 1)], else_=0)).label("member"),
                func.count(case([(User.user_type == 8) & (User.is_active == 1), 1], else_=0)).label("member_active"),
                func.count(case([(User.user_type == 8) & (User.is_active == 0), 1], else_=0)).label("member_inactive"),
                func.count(case([(User.is_active == 1, 1)], else_=0)).label("activeUsers"),
                func.count(case([(User.is_active == 0, 1)], else_=0)).label("inactiveUsers")
            )
            .filter(User.updated_at.between(fromdatetime, todatetime))
            .all()
        )
        return getTotalData

        

        # data = {
        #     "displayName":"Total Users",
        #     "key":"total_counts",
        #     "value":getTotalData.total,
        #     "colorCode":"#328CD1",
        #     "type":1,
        #     "leads":{"displayName":"Users","value":(getTotalData.total - len(getOverDue)) if user.user_type in 1,2 else getTotalData.total},
        #     "over_due":{"displayName":"Over Due","value":len(getOverDue)}if user.user_type in 1,2 else {}},
        #     {
        #     "displayName":"Assigned Users",
        #     "key":"assigned_count",
        #     "value":getTotalData.assigned,
        #     "colorCode":"#2AB95A",
        #     "type":2,
        #     "leads":{"displayName":"Users","value":getTotalData.assigned }},
         
        # {
        #     "displayName":"Total Quotation",
        #     "key":"quotation_count",
        #     "value":getTotalData.quotation,
        #     "colorCode":"#EB9C04",
        #     "leads":{"displayName":"Users","value":getTotalData.quotation },
            
        #     "type":4
        # },
        # {
        #     "displayName":"Total Followup",
        #     "key":"followup_count",
        #     "value":getTotalData.followup,
        #     "colorCode":"#FA5B62",
        #     "type":5,
        #     "leads":{"displayName":"Users","value":getTotalData.followup },
           
        # },
        # {
        #     "displayName":"Total Orders",
        #     "key":"orders_count",
        #     "value":getTotalData.orders,
        #     "colorCode":"#F87A05",
        #     "type":6,
        #     "leads":{"displayName":"Users","value":getTotalData.orders },
           
        # },
        # {
        #     "displayName":"Missed Users",
        #     "key":"missed_count",
        #     "value":getTotalData.missed,
        #     "colorCode":"#8154FF",
        #     "type":7,
        #     "leads":{"displayName":"Users","value":getTotalData.missed }
        # }
        
        return {"status":1,'msg':"Success.","data":data}
    else:
        return {"status":-1,"msg":"Sorry your login session expires.Please login again."}
