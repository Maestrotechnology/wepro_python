import datetime
from app.core.config import settings
from datetime import datetime
from app.core.config import settings
from app.models import *
import sys
import math
from pyfcm import FCMNotification
import smtplib
from app.models import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Environment, FileSystemLoader
from email.mime.image import MIMEImage
import os
import shutil
import smtplib
from email_validator import validate_email, EmailNotValidError
import tracemalloc
from pathlib import Path
from email.mime.application import MIMEApplication
tracemalloc.start()


def send_push_notification(db, user_ids, message, data_message=None):
    android_ids = []
    ios_ids = []

    get_users = (
        db.query(ApiTokens.push_device_id, ApiTokens.device_type)
        .filter(
            ApiTokens.user_id.in_(user_ids), ApiTokens.status == 1
        )
        .all()
    )

    for notify in get_users:
        if notify.push_device_id != None:
            if notify.device_type == 1:
                android_ids.append(notify.push_device_id)
            elif notify.device_type == 2:
                ios_ids.append(notify.push_device_id)


    push_service = FCMNotification(
            api_key="AAAAksKYbd8:APA91bE5SQ5t44lq1rHwvgL6--pWYauetRYV722ClO255j6XVUTHIE3rdo0ZoD8MxTwka9SJEfHQ3q2-2teuXbGSThBpC4Ai0DEgt9lJMWuo8p1ZkBGhVm9dwpWgizT00gpIRmpRa-pc"
        )
    message_title = message["msg_title"]
    message_body = message["msg_body"]

    if android_ids != []:
        # Android
        registration_ids = android_ids
        result = push_service.notify_multiple_devices(
            registration_ids=registration_ids,
            message_title=message_title,
            message_body=message_body,
            data_message=data_message
        )
    if ios_ids != []:
        # IOS
        result = push_service.notify_multiple_devices(
            registration_ids=ios_ids,
            message_title=message_title,
            message_body=message_body,
            data_message=data_message
        )


    return True


def get_timer(data):
    time1 = data.created_at
    time2 = datetime.now(settings.tz_IN)

    time_difference = (time2 - time1).total_seconds() / 60
    return (f"{int(time_difference)}")


def send_html_email(email_to: str, subject_template: str, html_template: str, environment: dict) -> None:
    from_email = settings.SENDER_EMAIL
    
    env = Environment(loader=FileSystemLoader("/"))
    template = env.from_string(html_template)

    html_content = template.render(environment)

    # ses = boto3.client(
    #     "ses",
    #     region_name="ap-south-1",
    #     aws_access_key_id=access_key,
    #     aws_secret_access_key=access_secret,
    # )
    # Prepare the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email_to
    msg['Subject'] = subject_template

    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, "bkdy ftou hcdx gwod") 
            server.sendmail(from_email, email_to, msg.as_string())
        # result = ses.send_raw_email(
        #     Source=msg["From"],
        #     Destinations=[email_to],
        #     RawMessage={"Data": msg.as_string()},
        # )
    except Exception as e:
        print(f"Error sending email: {e}")

async def send_mail_req_approval(db,email_type,article_id, user_id, subject,journalistName, receiver_email, message):
    from_email = settings.SENDER_EMAIL

    # Save email history to database
    addEmailHistory = EmailHistory(
        article_id=article_id ,
        user_id=user_id ,
        from_email=from_email,
        subject=subject,
        to_email=receiver_email,
        email_type = email_type,
        status=1,
        created_at=datetime.now(),
        message=message
    )
    db.add(addEmailHistory)
    db.commit()

    checkUserApp =db.query(User).filter(User.status==1,User.is_request==2,User.id==user_id).first()

    try:

        # Load the email template from the file
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ subject }}</title>
            <style>
                body {
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    -webkit-text-size-adjust: 100%;
                    -ms-text-size-adjust: 100%;
                }
                .container {
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #fff;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header {
                    text-align: center;
                    padding: 20px;
                    border-bottom: 1px solid #ddd;
                    background: url('http://35.154.143.177/WePRO_Digital.jpg') no-repeat center center;
                    background-size: cover;
                    height: 100px; /* Adjust based on your image height */
                }
                .header img {
                    max-width: 100%;
                    height: 80%;
                    pointer-events: none; /* Prevents image from being clickable */
                    user-select: none; /* Prevents text selection */
                }
                .content {
                    padding: 20px;
                    color: #333;
                    font-size: 16px;
                    line-height: 1.6;
                    background-color: #f9f9f9;
                }
                .content p {
                    margin: 0 0 20px;
                }
                .message {
                    text-indent: 20px;
                }
                .footer {
                    text-align: center;
                    color: #666;
                    padding: 10px;
                    font-size: 12px;
                    background-color: #f4f4f4;
                    border-top: 1px solid #ddd;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }

                /* Responsive adjustments */
                @media only screen and (max-width: 600px) {
                    .container {
                        width: 100% !important;
                        box-shadow: none;
                    }
                    .header {
                        padding: 10px;
                        font-size: 14px;
                        height: 80px; /* Adjust based on your image height */
                    }
                    .header img {
                        max-width: 100%;
                        height: auto;
                    }
                    .content {
                        padding: 15px;
                        font-size: 14px;
                    }
                    .footer {
                        padding: 10px;
                        font-size: 10px;
                    }
                }

                @media only screen and (max-width: 400px) {
                    .header {
                        padding: 8px;
                        height: 60px; /* Adjust based on your image height */
                    }
                    .header img {
                        max-width: 100%;
                        height: auto;
                    }
                    .content {
                        font-size: 12px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <!-- Uncomment the following line if you want to use an image instead of background -->
                    <!-- <img src="http://stgtal.jpg" alt="WePRO"> -->
                </div>
                <div class="content">
                    <p>Dear {{ name }},</p>
                    <p class="message">{{ message }}</p>

                    {% if attachment_link %}
                <p>We've included a <strong>{{ attachment_name }}</strong> to help you get started and understand our working process. <a href="{{ attachment_link }}" download>Click here to open the attachment</a> and learn more about how you can contribute to our community.</p>
                {% endif %}
                    <p>Warm regards,<br>Team WePRO.Digital</p>
                </div>
                <div class="footer">
                    <p>&copy; {{ current_year }} WePRO. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        attachment=None
        userType=None
        attachmentLink =None
        attachmentName =None

        if checkUserApp and email_type==1:
            attachment=1
            if checkUserApp.user_type==8:
                attachmentLink = f"{settings.BASE_DOMAIN}/welcome_letter.pdf"
                attachmentName ="welcome Letter"

                


        send_html_email(
            email_to=receiver_email,
            subject_template=subject,
            html_template=html_template,
            environment={
                "name":journalistName,
                "message": message,
                "subject": subject,
                "current_year": datetime.now(settings.tz_IN).year,
                "email": receiver_email,
                "attachment_link": attachmentLink,
                 "attachment_name": attachmentName

            }
        )
        addEmailHistory.response = "success"
        db.commit()

        return {"status": 1, "msg": "Success"}

    except Exception as e:
        db.rollback()
        
        addEmailHistory.response = f"Failed to send email: {str(e)}"
        db.commit()
        return {"status": 0, "msg": f"Failed to send email: {str(e)}"}

        
   
    

async def send_mail(db,receiver_email, message):  # Demo
    sender_email = "johnsonkoilraj53@gmail.com"
    receiver_email = receiver_email
    password = "bkdy ftou hcdx gwod"

    msg = MIMEText(message)

    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Otp "

    # msg = str(message)
    addEmailHistory = EmailHistory(
        from_email=sender_email,
        subject="OTP",
        to_email=receiver_email,
        status=1,
        created_at = datetime.now(settings.tz_IN),
        message = message
    )
    db.add(addEmailHistory)
    db.commit()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


    return True


def file_storage(file_name, f_name):

    base_dir = settings.BASE_UPLOAD_FOLDER+"/file_wepro"

    dt = str(int(datetime.utcnow().timestamp()))

    try:
        os.makedirs(base_dir, mode=0o777, exist_ok=True)
    except OSError as e:
        sys.exit("Can't create {dir}: {err}".format(
            dir=base_dir, err=e))

    output_dir = base_dir + "/"

    filename = file_name.filename
    # Split file name and extension

    txt = filename[::-1]
    splitted = txt.split(".", 1)
    txt1 = splitted[0][::-1]
    # txt2 = splitted[1][::-1]

    files_name = f_name.split(".")

    save_full_path = f'{output_dir}{files_name[0]}{dt}.{txt1}'
    print(save_full_path)


    file_exe = f"file_wepro/{f_name}{dt}.{txt1}"
    with open(save_full_path, "wb") as buffer:
        shutil.copyfileobj(file_name.file, buffer)
    encoded_data=None

    # import base64
    # with open(save_full_path, "rb") as buffer:
    #     file_data = buffer.read()  # Read the raw file data
    #     encoded_data = base64.b64encode(file_data).decode('utf-8')
    return save_full_path, file_exe


def store_file(file):

    base_dir = settings.BASE_UPLOAD_FOLDER+"/upload_files/"

    dt = str(int(datetime.utcnow().timestamp()))

    try:
        os.makedirs(base_dir, mode=0o777, exist_ok=True)
    except OSError as e:
        sys.exit("Can't create {dir}: {err}".format(
            dir=base_dir, err=e))

    filename = file.filename

    file_properties = filename.split(".")

    file_extension = file_properties[-1]

    file_properties.pop()
    file_splitted_name = file_properties[0]

    write_path = f"{base_dir}{file_splitted_name}{dt}.{file_extension}"
    db_path = f"/upload_files/{file_splitted_name}{dt}.{file_extension}"

    with open(write_path, "wb") as new_file:
        shutil.copyfileobj(file.file, new_file)

    return db_path


def pagination(row_count=0, page=1, size=10):
    current_page_no = page if page >= 1 else 1

    total_pages = math.ceil(row_count / size)

    if current_page_no > total_pages:
        current_page_no = total_pages

    limit = current_page_no * size
    offset = limit - size

    if limit > row_count:
        limit = offset + (row_count % size)

    limit = limit - offset

    if offset < 0:
        offset = 0

    return [limit, offset]


def get_pagination(row_count=0, current_page_no=1, default_page_size=10):
    current_page_no = current_page_no if current_page_no >= 1 else 1

    total_pages = math.ceil(row_count / default_page_size)

    if current_page_no > total_pages:
        current_page_no = total_pages

    limit = current_page_no * default_page_size
    offset = limit - default_page_size

    if limit > row_count:
        limit = offset + (row_count % default_page_size)

    limit = limit - offset

    if offset < 0:
        offset = 0

    return [total_pages, offset, limit]


def paginate(page, size, data, total):
    reply = {"items": data, "total": total, "page": page, "size": size}
    return reply


def paginate_for_file_count(page, size, data, total, file_count):
    reply = {"items": data, "total": total, "page": page,
             "file_count": file_count, "size": size}
    return reply



def common_date(date, without_time=None):

    datetime = date.strftime("%d-%m-%Y %I:%M:%S")

    if without_time == 1:
        datetime = date.strftime("%d-%m-%Y")
    if without_time == 2:
        datetime = date.strftime("%I:%M:%S")

    return datetime


def check(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError as e:
        return False

def convert_tz(time_data, from_zone: str, to_zone: str) -> datetime:

    # METHOD 1: Hardcode zones:
    # from_zone = tz.gettz('UTC')
    # to_zone = tz.gettz('Asia/Kolkata')

    from_zn = from_zone.split(' (') if from_zone else None
    to_zn = to_zone.split(' (') if from_zone else None

    from_zone = tz.gettz(from_zn[0])
    to_zone = tz.gettz(to_zn[0])

    # METHOD 2: Auto-detect zones:
    # from_zone = tz.tzutc()
    # to_zone = tz.tzlocal()

    # utc1 = datetime.utcnow()
    from_time = time_data
    if type(time_data) == str:
        try:
            from_time = datetime.strptime(time_data, '%Y-%m-%d %H:%M:%S')
        except:
            from_time = datetime.strptime(time_data, '%Y-%m-%dT%H:%M:%S')
    from_time_zone = from_time.replace(tzinfo=from_zone, microsecond=0)

    # Convert time zone
    to_time = from_time_zone.astimezone(to_zone)

    return to_time.replace(tzinfo=None)
