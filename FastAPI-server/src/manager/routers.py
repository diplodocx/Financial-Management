from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
import src.manager.queries as queries
from .schemas import CategoryGet, PaymentGet, PaymentPost
from typing import List

manager = APIRouter(
    prefix="/manager",
    tags=['manager']
)


@manager.get("/category", response_model=List[CategoryGet])
async def get_category(session: AsyncSession = Depends(get_async_session)):
    return await queries.select_categories(session)


@manager.get("/category/{category_id}", response_model=CategoryGet)
async def retrieve_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    return await queries.select_category(category_id, session)


@manager.get("/payment", response_model=List[PaymentGet])
async def get_payment(session: AsyncSession = Depends(get_async_session)):
    return await queries.select_payments(session)


@manager.get("/payment/{payment_id}", response_model=PaymentGet)
async def retrieve_payment(payment_id: int, session: AsyncSession = Depends(get_async_session)):
    return await queries.select_payment(payment_id, session)


@manager.post("/payment")
async def get_payment(payment: PaymentPost, session: AsyncSession = Depends(get_async_session)):
    return await queries.insert_payment(payment, session)

@manager.delete("/payment/{payment_id}")
async def delete_payment(payment_id: int, session: AsyncSession = Depends(get_async_session)):
    return await queries.delete_payment(payment_id, session)
