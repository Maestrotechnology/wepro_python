from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from datetime import date,timedelta
from app.utils import *
from sqlalchemy import or_,func,case,extract,cast,Date,distinct

import random


router = APIRouter()


import calendar

# @router.post("/add_sub_category")
# async def subCat(db:Session = Depends(deps.get_db),):
#     all_categories = [
#     {
#         "category": "BUSINESS",
#         "subcategories": [
#             "Entrepreneurship",
#             "Ownership",
#             "Female Founders",
#             "Finance",
#             "Financial Independence",
#             "Human Resources",
#             "Leadership",
#             "Innovation",
#             "Business Women",
#             "Business Trends",
#             "Small Business",
#             "Online Business",
#             "Business Development",
#             "Skills Development",
#             "Business Planning",
#             "Digital Marketing",
#             "Workplace",
#             "Women Empowerment",
#             "Gender Equality",
#             "Women in charge"
#         ]
#     },
#     {
#         "category": "SCI-TECH",
#         "subcategories": [
#             "Women in Tech",
#             "Women in STEM",
#             "Artificial Intelligence",
#             "Women in AI",
#             "Cybersecurity",
#             "Science and Technology",
#             "Environment",
#             "Future Women",
#             "Innovation",
#             "Women and Healthcare",
#             "Tech and Body positivity",
#             "STEM Education",
#             "Scientific Breakthroughs",
#             "Female Scientists",
#             "Inclusive Tech",
#             "Women Led Tech-startups",
#             "Technology Business",
#             "Tech Trends"
#         ]
#     },
#     {
#         "category": "START UPS",
#         "subcategories": [
#             "Women Start-ups",
#             "Start-up Ecosystem",
#             "Start-up Advice",
#             "Tech Start-ups",
#             "Health Start-ups",
#             "Start-up Resources",
#             "Success Stories",
#             "Small Business",
#             "Affordability",
#             "Innovation & Creativity",
#             "Growth",
#             "Social Impact",
#             "Women in Finance",
#             "Sustainability",
#             "E-commerce",
#             "Women Entrepreneurs",
#             "Networking"
#         ]
#     },
#     {
#         "category": "LIFESTYLE",
#         "subcategories": [
#             "Clean Living",
#             "Sustainable Living",
#             "Sustainability",
#             "Environmental Choices",
#             "Eco-friendly Living",
#             "DIYs",
#             "Tips & Hacks",
#             "Personal Care",
#             "Budget Planning",
#             "Saving Strategies",
#             "Relationships",
#             "Parenting",
#             "Communication Skills",
#             "Holistic Lifestyle",
#             "Fashion",
#             "Makeup and Skincare",
#             "Sustainable Fashion",
#             "Travel",
#             "Travel Tips and Guides",
#             "Home Organization",
#             "Home Essentials",
#             "Work-Life Balance"
#         ]
#     },
#     {
#         "category": "EDUCATION",
#         "subcategories": [
#             "Education and Women",
#             "Women in STEM",
#             "Career-Oriented Education",
#             "Continuing Education",
#             "Mentorship and Coaching",
#             "Self-Improvement",
#             "Learning Opportunities",
#             "Online Learning",
#             "Awareness",
#             "Media Literacy",
#             "Finance Literacy",
#             "Scholarships for Women",
#             "Gender Studies",
#             "Women’s Issues",
#             "Educating Women’s Issues",
#             "Community Development",
#             "Teaching Profession",
#             "Advocacy for Women in Education",
#             "Access and Equity",
#             "Educational Rights for Women"
#         ]
#     },
#     {
#         "category": "HEALTH",
#         "subcategories": [
#             "Mental Health",
#             "Stress Management",
#             "Anxiety Management",
#             "Emotional Well-being",
#             "Work-Life balance",
#             "Self-Care",
#             "Mindfulness",
#             "Meditation",
#             "Resilience Building",
#             "Physical Health",
#             "Exercise for Women",
#             "Home Workouts",
#             "Fitness for Different Life Stages",
#             "Menstruation",
#             "Menstrual Health",
#             "Sexual Health and Wellness",
#             "Pregnancy",
#             "Reproductive Health",
#             "Lifestyle Modification",
#             "Nutrition",
#             "Balanced Diet Choices",
#             "Cooking for Health"
#         ]
#     },
#     {
#         "category": "NATURE",
#         "subcategories": [
#             "Sustainable Products",
#             "Sustainable practices",
#             "Sustainable Fashion",
#             "Waste Reduction",
#             "Recycling",
#             "Zero-waste Practices",
#             "Energy Conservation",
#             "Nature Retreats for Women",
#             "Gardening",
#             "Home Gardening",
#             "Gardening for Mental Health",
#             "Women and Environment",
#             "Women-led Conservation Projects",
#             "Women’s Impact on Environment",
#             "Benefits of Nature",
#             "Ecofeminism",
#             "Environmental Activism",
#             "Climate Change"
#         ]
#     },
#     {
#         "category": "SPORTS",
#         "subcategories": [
#             "Outdoor Sports",
#             "Indoor Sports",
#             "Women Athletes",
#             "Women in Sports",
#             "Women achievers in Sports",
#             "Sports News and Events",
#             "Women’s Cricket",
#             "Women’s Sports",
#             "Nutrition for Sports",
#             "Senior Athletes",
#             "Rising Athletes",
#             "Book of Record"
#         ]
#     },
#     {
#         "category": "WORLD",
#         "subcategories": [
#             "Global Women’s Rights",
#             "Women and Culture",
#             "World News on Women",
#             "Inspirational Women",
#             "World News",
#             "World Leaders",
#             "Cultural Events",
#             "World Entertainment",
#             "Pop culture",
#             "Infotainment",
#             "Feminism",
#             "Women Empowerment",
#             "Women in Media",
#             "World Economy",
#             "International Law for Women",
#             "Women in Cinema",
#             "Women in History",
#             "Global Trends",
#             "Human Rights",
#             "Global Health"
#         ]
#     },
#     {
#         "category": "ENTERTAINMENT",
#         "subcategories": [
#             "Movies and TV",
#             "Female Characters",
#             "Women in Cinema",
#             "TV shows",
#             "Web Series",
#             "Documentaries",
#             "Music",
#             "Music Therapy",
#             "Women in Music",
#             "Indie Music",
#             "Books and Literature",
#             "Women Authors",
#             "Social Media",
#             "Social Media Trends",
#             "Celebrity style",
#             "Influencer Culture",
#             "Events",
#             "Women’s Events",
#             "Women and Art",
#             "Podcasts"
#         ]
#     },
#     {
#         "category": "HISTORY",
#         "subcategories": [
#             "Trailblazers",
#             "Hidden figures",
#             "Women’s Suffrage Movement",
#             "Freedom Struggle",
#             "Ancient History",
#             "Modern History",
#             "Women in World Wars",
#             "History of Women",
#             "Social History",
#             "Economic History",
#             "Women and Ancestry",
#             "Women in Literature",
#             "Women’s History Month",
#             "Women’s Rights",
#             "Gender Equality",
#             "Women and Civil Rights",
#             "Women in Music",
#             "Historical Women",
#             "Fight for Women",
#             "Feminism Movement",
#             "Women in Medicine"
#         ]
#     }
# ]
#     for row in all_categories:
#         print(row["category"])

#         addCategory = Category(
#             title = row["category"],
#             status=1,
#             is_active=1,
#             created_at = datetime.now(settings.tz_IN),
#             created_by =1)

#         db.add(addCategory)
#         db.commit()

#         for ij in row["subcategories"]:
#             print(ij)
#             addSubCategory = SubCategory(
#             title = ij,
#             category_id = addCategory.id,
#             status=1,
#             created_at = datetime.now(settings.tz_IN),
#             created_by = 1)

#             db.add(addSubCategory)
#             db.commit()




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

            totalArticle = db.query(func.count(distinct(ArticleHistory.article_id))).filter(
                cast(ArticleHistory.created_at, Date) == current_date,
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
                ArticleHistory.chief_editor_id==user.id,
                                               )
                articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)
                
            if user.user_type==5:

                totalArticle=totalArticle.filter(
                ArticleHistory.sub_editor_id==user.id,
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

            totalArticle = db.query(func.count(distinct(ArticleHistory.article_id))).filter(
                cast(ArticleHistory.created_at, Date) == current_date,
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
                ArticleHistory.chief_editor_id==user.id,
                                               )
                
                articleAction = articleAction.filter(ArticleHistory.chief_editor_id==user.id)

                
            if user.user_type==5:

                totalArticle=totalArticle.filter(
                ArticleHistory.sub_editor_id==user.id,
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
