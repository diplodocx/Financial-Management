from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from .reports import make_report, send_report

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
    send_report.delay(user_id)
    return {"detail": "task delegated"}