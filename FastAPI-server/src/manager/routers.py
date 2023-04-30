from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
import src.manager.queries as queries
from .schemas import CategoryGet
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
