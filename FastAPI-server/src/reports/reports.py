import pandas as pd
from celery import Celery
from sqlalchemy.orm import Session
from .database import get_session
from .queries import select_payments, select_last_report

app = Celery('tasks', broker="redis://localhost:6379", backend="redis://localhost:6379")


@app.task()
def make_report(user_id, session: Session = next(get_session())):
    rows, columns = select_payments(user_id, session)
    last_report = select_last_report(user_id, session)
    df = pd.DataFrame(rows, columns=columns)
    df['payment_time'] = df['payment_time'].apply(lambda x: x.strftime('%d.%m.%Y %H:%M:%S'))
    df.to_excel(f'./src/reports/data/{user_id}_data_{last_report + 1}.xlsx', index=False)
