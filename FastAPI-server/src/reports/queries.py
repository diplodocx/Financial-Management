from sqlalchemy.orm import Session
from src.manager.models import user, category, payment
import sqlalchemy as db
from sqlalchemy.orm.exc import NoResultFound


def select_payments(user_id, session: Session):
    stmt = db.select(payment).where(payment.c.owner == user_id)
    result = session.execute(stmt)
    if not result:
        raise NoResultFound
    return result.fetchall(), result.keys()


def select_last_report(user_id, session: Session):
    stmt = db.select(user.c.last_report).where(user.c.id == user_id)
    result = session.execute(stmt)
    if not result:
        raise NoResultFound
    last_report = result.fetchone()[0]
    update_last_report(user_id, last_report, session)
    return last_report


def update_last_report(user_id, last_report, session: Session):
    stmt = db.update(user).where(user.c.id == user_id).values(last_report=last_report+1)
    session.execute(stmt)
