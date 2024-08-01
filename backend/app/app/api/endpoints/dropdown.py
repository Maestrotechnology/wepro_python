from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.utils import *

router = APIRouter()
    
@router.post("/user_dropdown")
async def userDropdown(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       user_type:int=Form(None),is_report:int=Form(None)):
    user = deps.get_user_token(db=db,token =token)
    if user:
        if user:
           
            getUser = db.query(User)
            if is_report:
                getUser = getUser
            else:
                getUser = getUser.filter(User.status == 1)


            if user_type :
                getUser = getUser.filter(User.user_type == user_type)

            
            getUser = getUser.order_by(User.name.asc()).all()

            dataList =[]

            if getUser:
                for userData in getUser:
                    dataList.append({
                        "user_id":userData.id,
                        "user_name":f"{userData.name} ({userData.phone})"
                    })
            return {"status":1,"msg":"Success","data":dataList}
        else:
            return {"status":0,"msg":"You are not authenticated to see the user details."}
    return {'status':-1,"msg":"Your login session expires.Please login later."}


@router.post("/state_dropdown")
async def stateDropDown(db:Session = Depends(deps.get_db),
                           token:str=Form(...)):
    user = deps.get_user_token(db=db,token =token)
    if user:
        # statesList =[22,36,19,17,35]
        getAllState = db.query(States).filter(States.status==1).order_by(States.name.asc()).all()
        dataList =[]
        if getAllState:
            for row in getAllState:
                dataList.append({
                    "stateId":row.id,
                    "stateName":row.name
                })
        return {"status":1,"msg":"Success","data":dataList}
    return {'status':-1,"msg":"Your login session expires.Please login later."}



@router.post("/city_dropdown")
async def cityDropDown(db:Session = Depends(deps.get_db),
                           token:str=Form(...),stateId:int=Form(None)):
    user = deps.get_user_token(db=db,token =token)
    if user:
        getAllCity = db.query(Cities).filter(Cities.status==1)

        if stateId:
            getAllCity = getAllCity.filter(Cities.state_id == stateId)
        getAllCity = getAllCity.order_by(Cities.name.asc()).all()

        dataList =[]
        if getAllCity:
            for row in getAllCity:
                dataList.append({
                    "cityId":row.id,
                    "cityName":row.name
                })
        return {"status":1,"msg":"Success","data":dataList}
    return {'status':-1,"msg":"Your login session expires.Please login later."}


@router.post("/topic_dropdown")
async def topicDropDown(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       category_id:int=Form(None)):
    user = deps.get_user_token(db=db,token =token)
    if user:
        if user:

            getArticleTopic = db.query(ArticleTopic).filter(ArticleTopic.status == 1)

            count = getArticleTopic.count()

            if category_id:
                getArticleTopic =getArticleTopic.filter(ArticleTopic.category_id==category_id)
                
            getArticleTopic = getArticleTopic.order_by(ArticleTopic.topic.asc()).all()
            
            dataList =[]

            if getArticleTopic:
                for topic in getArticleTopic:
                    dataList.append({
                        "topic_id":topic.id,
                        "category_id":topic.category_id,
                        "topic":topic.topic
                    })

            return {"status":1,"msg":"Success","data":dataList}
        else:
            return {"status":0,"msg":"You are not authenticated to see the Editors's Topic."}
    return {'status':-1,"msg":"Your login session expires.Please login later."}


@router.post("/category_dropdown")
async def categoryDropDown(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       is_report:int=Form(None)):
    user = deps.get_user_token(db=db,token =token)
    if user:
        if user:

            getCategory = db.query(Category).filter(Category.status == 1)


            if not is_report:
                getCategory = getCategory.filter(Category.is_active==1)

            count = getCategory.count()
            getCategory = getCategory.order_by(Category.title.asc()).all()
            

            dataList =[]

            if getCategory:
                for category in getCategory:
                    dataList.append({
                        "category_id":category.id,
                        "title":category.title
                    })

            return {"status":1,"msg":"Success","data":dataList}
        else:
            return {"status":0,"msg":"You are not authenticated to see the Category details."}
    return {'status':-1,"msg":"Your login session expires.Please login later."}


@router.post("/sub_category_dropdown")
async def subCtegoryDropDown(db:Session=Depends(deps.get_db),
                       token:str=Form(...),
                       category_id:int=Form(None)
                ):
    user = deps.get_user_token(db=db,token =token)
    if user:
        if user:

            getSubCategory = db.query(SubCategory).filter(SubCategory.status == 1)

            if category_id:
                getSubCategory =getSubCategory.filter(SubCategory.category_id == category_id)


            # if not is_report:
            #     getSubCategory = getSubCategory.filter(SubCategory.is_active==1)


            count = getSubCategory.count()

            getSubCategory = getSubCategory.order_by(SubCategory.title.asc()).all()
            

            dataList =[]


            if getSubCategory:
                for category in getSubCategory:
                    dataList.append({
                        "sub_category_id":category.id,
                        "title":category.title
                    })

            return {"status":1,"msg":"Success","data":dataList}
        else:
            return {"status":0,"msg":"You are not authenticated to see the Sub Category details."}
    return {'status':-1,"msg":"Your login session expires.Please login later."}

