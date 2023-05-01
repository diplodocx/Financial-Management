import sqlalchemy as db
from celery import Celery
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from src.manager.models import user, category, payment

from database import DATABASE_URL

celery = Celery('tasks', broker="redis://localhost:6379")

@celery.task()
def make_report(user_id):
    engine = create_engine("sqlite:///manager.db")
    with engine.begin() as conn:
        stmt = db.select(payment).where(payment.c.owner == user_id)
        result = conn.execute(stmt)
        rows = result.fetchall()
    df = pd.DataFrame(rows, columns=result.keys())
    df['payment_time'] = df['payment_time'].apply(lambda x: x.strftime('%d.%m.%Y %H:%M:%S'))
    print(df)
    df.to_excel('data.xlsx', index=False)
