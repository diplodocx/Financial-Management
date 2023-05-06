from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_session
from .reports import make_report

reports = APIRouter(prefix='/report', tags=['report'])

@reports.get('/{user_id}')
def get_reports(user_id: int):
    make_report.delay(user_id)
    return {"detail": "report generated"}