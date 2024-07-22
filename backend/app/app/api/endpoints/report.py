
from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import ApiTokens,User
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_,func,case,extract
from app.core import security
import xlsxwriter


import random


router = APIRouter()



@router.post("/articleReport")
async def articleReport(db:Session=Depends(deps.get_db),
                     token:str = Form(...),fromDateTime :datetime=Form(None),
                     toDatetime : datetime = Form(None),
                     journalist_id:int=Form(None),
                     state_id:int=Form(None),
                     city_id:int=Form(None)):
    user = deps.get_user_token(db=db,token=token)
    if user:
        # currentYear = year or datetime.now(settings.tz_IN).year
        today = datetime.now(settings.tz_IN)

        if toDatetime == None:
            toDatetime = today.replace(hour=23,minute=59,second=59)
   
        else:
            toDatetime = toDatetime.replace(hour=23,minute=59,second=59)
        if fromDateTime == None:
            fromDateTime = today.replace(day=1,month=1,hour=0,minute=0,second=0)
        else:
            fromDateTime = fromDateTime.replace(hour=0,minute=0,second=0)
        
        getTotalData = (
             db.query(
                extract('month',Article.created_at).label('month'),
                func.count(case((Article.status == 1, 1))).label("total"),
                func.count(case((Article.content_approved == 1, 1))).label("new"),
                func.count(case((Article.content_approved == 0, 1))).label("not_submitted"),
                func.count(case((Article.content_approved == 3, 1))).label("published"),
                func.count(case((Article.content_approved == 4, 1))).label("on_hold"),
            ) ).filter(Article.status == 1)
        
      
        getTotalData = getTotalData.filter(Article.created_at.between(fromDateTime,toDatetime))
        
        if journalist_id:
          
            getTotalData = getTotalData.filter(Article.created_by == journalist_id )

        if state_id:
            getTotalData = getTotalData.filter(Article.state_id == state_id)
        
        if city_id:
            getTotalData = getTotalData.filter(Article.city_id == city_id)

        getTotalData = getTotalData.group_by(extract('month',Article.created_at)).all()
        
        result_by_month={}
        formatted_result =[]
      
        if getTotalData:
            for month,total,new,not_submitted,published,on_hold in getTotalData:

                if month not in result_by_month:
                    result_by_month[month] = {"total": 0,"new":0,"not_submitted":0,"published":0,"on_hold":0}
                        
                result_by_month[month]["total"] = total
                result_by_month[month]["new"] = new
                result_by_month[month]["not_submitted"] = not_submitted
                result_by_month[month]['published'] = published
                result_by_month[month]["on_hold"] = on_hold
       
        
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
            new = data["new"]
            not_submitted =data["not_submitted"]
            published = data["published"]
            on_hold = data["on_hold"]

        else:
            total = 0
            new = 0
            not_submitted = 0
            published = 0
            on_hold = 0
        import calendar
        # totalCount = open + assigned + demo +  quotation + follow_up + close + order
        formatted_result.append({
                # "month": month,
                "month": calendar.month_name[month],

                "Total":total,
                "New":new,
                "Not Submitted":not_submitted,
                "Published":published,
                "On Hold":on_hold,
                "successPercentage":(published/total)*100 if published!=0 else 0})
        
    return formatted_result
 

@router.post("/journalist_performance")
async def journalistPerformance(db:Session=Depends(deps.get_db),token:str=Form(...),journalist_id:int=Form(None),
                                state_id:int=Form(None),city_id:int=Form(None),
                                fromDatetime:datetime=Form(None),toDatetime:datetime=Form(None),page:int=1,size:int=10,
                                is_report:int=Form(None,description="1-for xl")):
    user = deps.get_user_token(db=db,token=token)
    if user:
        today = datetime.now()
        if not fromDatetime:
            fromDatetime = today.replace(day=1,month=1,hour=0,minute=0,second=0)
        else:
            fromDatetime = fromDatetime.replace(hour=0,minute=0,second=0)
        if not toDatetime:
            toDatetime = today.replace(hour=23,minute=59,second=59)
        else:
            toDatetime = toDatetime.replace(hour=23,minute=59,second=59)

        getAllJournalist =  db.query(User).filter(User.status==1,User.user_type == 7)
        if journalist_id:
            getAllJournalist = getAllJournalist.filter(User.id == journalist_id)

        
        if state_id:
            getAllJournalist = getAllJournalist.filter(User.state_id==state_id)

        if city_id:
            getAllJournalist = getAllJournalist.filter(User.city_id==city_id)


        totalCount = getAllJournalist.count()
        if is_report!=1:
            totalPage,offset,limit = get_pagination(totalCount,page,size)
            getAllJournalist = getAllJournalist.order_by(User.id.desc()).limit(limit).offset(offset).all()

        dataList =[]
        for journalist in getAllJournalist:

            total,published,on_hold=getJournalistData(db,fromDatetime,toDatetime,journalist.id)
            if total == 0 and published == 0:
                total = 1
            dataList.append({
                "Journalist_name":journalist.name,
                "journalist_id": journalist.id,
                "total_article":total,
                "on_hold_article":on_hold,
                "published_article":published,
                "successPercentage": (published/total) *100 ,
                "phone":journalist.phone,
                "email":journalist.email,
                "bank":journalist.bank,
                "ifsc_code":journalist.ifsc_code,
                "branch":journalist.branch,
                "account_number":journalist.account_number,
  
            })

        if is_report!=1:
    
            data=({"page":page,"size":size,
                        "total_page":totalPage,
                        "total_count":totalCount,
                        "items":dataList})
            return ({"status":1,"msg":"Success","data":data})
        
        base_dir = settings.BASE_UPLOAD_FOLDER + "/"
        try:
            os.makedirs(base_dir, mode=0o777, exist_ok=True)
        except OSError as e:
            sys.exit("Can't create {dir}: {err}".format(dir=base_dir, err=e))

        output_dir = base_dir + settings.BASE_DIR + "/journal_report/"
        out_dir_2 = f"{settings.BASE_DIR}/journal_report/"
        try:
            os.makedirs(output_dir, mode=0o777, exist_ok=True)
        except OSError as e:
            sys.exit("Can't create {dir}: {err}".format(dir=output_dir, err=e))

        dt = str(int(datetime.utcnow().timestamp()))
        file_name = f"station_report{dt}.xlsx"

        fileName = f"{output_dir}journalist_report{dt}.xls"
        fileName2 = f"{out_dir_2}journalist_report{dt}.xls"

        headers = [
            [
                "S.No",
                "Journalist Name",
                "Phone",
                "Email",
                "Total Article",
                "On Hold",
                "Published",
                "Account Number",
                "Ifsc Code",
                "Bank",
                "Branch"
            ]
        ]
        sr_no = 0
        for row in dataList:
            datas = []
            sr_no += 1

            datas.append(str(sr_no))
            datas.append(
                str(
                    row["Journalist_name"]
                    if row["Journalist_name"] != None and row["Journalist_name"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["phone"]
                    if row["phone"] != None and row["phone"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["email"]
                    if row["email"] != None and row["email"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["total_article"]
                    if row["total_article"] != None and row["total_article"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["on_hold_article"]
                    if row["on_hold_article"] != None
                    and row["on_hold_article"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["published_article"]
                    if row["published_article"] != None and row["published_article"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["account_number"]
                    if row["account_number"] != None and row["account_number"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["ifsc_code"]
                    if row["ifsc_code"] != None and row["ifsc_code"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["bank"]
                    if row["bank"] != None and row["bank"] != ""
                    else "-"
                )
            )
            datas.append(
                str(
                    row["branch"]
                    if row["branch"] != None and row["branch"] != ""
                    else "-"
                )
            )
            headers.append(datas)

        with xlsxwriter.Workbook(fileName) as workbook:
            worksheet = workbook.add_worksheet()
            merge_format = workbook.add_format(
                {"bold": 1, "border": 1, "align": "left", "valign": "vcenter"}
            )
            merge_format_row = workbook.add_format(
                {
                    "align": "center",
                    # 'bold': 0.5,
                    "valign": "vcenter",
                }
            )
            merge_format_row2 = workbook.add_format(
                {"align": "left", "valign": "vcenter"}
            )
            merge_format_head = workbook.add_format(
                {
                    "bold": 0.5,
                    "border": 1,
                    "align": "center",
                    "valign": "vcenter",
                    "fg_color": "#808080",
                }
            )
            header_change = workbook.add_format(
                {
                    "bold": 1,
                    "align": "center",
                }
            )
            logo_left_side = workbook.add_format(
                {"align": "center", "font_size": "10px"}
            )
            footer = workbook.add_format(
                {"bold": 1, "align": "center", "font_size": "10px"}
            )
            logo_center_side = workbook.add_format(
                {"align": "center", "font_size": "10px"}
            )

            image_path =  os.path.realpath(
                f"{settings.BASE_UPLOAD_FOLDER}/WePRO_Digital.jpg")

            # Convert JPG to PNG
            # Image.open(jpg_file).convert('RGB').save(png_file)
            # worksheet.insert_image('B2:C2',image_path,{'x_offset': 0, 'y_offset': 0, 'x_scale': 0.40, 'y_scale': 0.3})
            worksheet.insert_image('B2:C2',image_path,{'x_offset': 0, 'y_offset': 0, 'x_scale': 0.40, 'y_scale': 0.4})

            worksheet.merge_range("D2:L2", f"JOURNALIST REPORT", header_change)

            lst = 0

            for i, l in enumerate(headers):
                i += 4
                lst += i
                for j, col in enumerate(l):
                    j += 1
                    if i == 4:
                        worksheet.write(i, j, col, merge_format_head)
                    else:
                        worksheet.write(i, j, col, merge_format_row)

            my_format = workbook.add_format()
            my_format.set_align("vcenter")
            worksheet.set_column("B:XFC", 15, my_format)


        return {
                "status": 1,
                "msg": "Success",
                "file_path":f"{settings.BASE_DOMAIN}{fileName2}"}
        

    else:
        return {"status":-1,"msg":"Sorry your login session expires.Please login again."}


def getJournalistData(db:Session,fromdatetime,todatetime,journalist_id:int):

    getTotalData = (
            db.query(
                func.count(case((Article.status == 1, 1))).label("total"),
                func.count(case((Article.content_approved == 3, 1))).label("published"),
                func.count(case((Article.content_approved == 4, 1))).label("on_hold"),
                # func.count(case([(Article.content_approved == 17, 1)])).label("notValid")
            ) ).filter(Article.created_at.between(fromdatetime,todatetime),Article.status == 1)
        
    
    getTotalData = getTotalData.filter(Article.created_by == journalist_id )
    getTotalData = getTotalData.all()

    if getTotalData:
        for data in getTotalData:
            return data.total,data.published,data.on_hold
    return 0,0,0

