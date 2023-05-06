from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_session
from .reports import make_report
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException

reports = APIRouter(prefix='/report', tags=['report'])

@reports.get('/{user_id}')
def get_reports(user_id: int):
    result = make_report.delay(user_id)
    try:
        result.get()
    except NoResultFound:
        raise HTTPException(status_code=404)
    except:
        raise HTTPException(status_code=500)
    return {"detail": "task delegated"}