from fastapi import HTTPException

from .models import category, payment, user
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as db


async def select_categories(session: AsyncSession):
    stmt = db.select(category)
    res = await session.execute(stmt)
    return res.mappings().fetchall()


async def select_category(category_id, session: AsyncSession):
    stmt = db.select(category).where(category.c.category_id == category_id)
    res = await session.execute(stmt)
    element = res.mappings().fetchone()
    if not element:
        raise HTTPException(status_code=404, detail="Item not found")
    return element

