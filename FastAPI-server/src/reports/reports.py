from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from celery import Celery, Task
from sqlalchemy.orm import Session
from .database import get_session
from .queries import select_payments, select_last_report, update_last_report
import smtplib
from config import SMTP_PASSWORD, SMTP_USER


app = Celery('tasks', broker="redis://localhost:6379", backend="redis://localhost:6379")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


@app.task()
def make_report(user_id, session: Session = next(get_session())):
    rows, columns = select_payments(user_id, session)
    last_report = select_last_report(user_id, session)
    update_last_report(user_id, last_report, session)
    df = pd.DataFrame(rows, columns=columns)
    df['payment_time'] = df['payment_time'].apply(lambda x: x.strftime('%d.%m.%Y %H:%M:%S'))
    df.to_excel(f'./src/reports/data/{user_id}_data_{last_report + 1}.xlsx', index=False)


@app.task()
def make_template(user_id: int, last_report: int):
    msg = MIMEMultipart()
    msg['Subject'] = 'Расходы'
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER
    body = 'Вот ваши расходы:'
    msg.attach(MIMEText(body, 'plain'))
    filename = f"{user_id}_data_{last_report}.xlsx"
    with open(f'./src/reports/data/{filename}', "rb") as f:
        attach = MIMEApplication(f.read(), _subtype='xlsx')
        attach.add_header('Content-Disposition', 'attachment', filename=str(filename))
        msg.attach(attach)
    return msg

@app.task()
def send_report(user_id, session: Session = next(get_session())):
    last_report = select_last_report(user_id, session)
    msg = make_template(user_id, last_report)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
