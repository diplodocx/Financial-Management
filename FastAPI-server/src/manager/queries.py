from fastapi import HTTPException
from starlette.responses import JSONResponse

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


async def select_payments(session: AsyncSession):
    stmt = db.select(payment, category).join(category, category.c.category_id == payment.c.category)
    res = await session.execute(stmt)
    return res.mappings().fetchall()


async def select_payment(payment_id: int, session: AsyncSession):
    stmt = db.select(payment, category).join(category, category.c.category_id == payment.c.category) \
        .where(payment.c.payment_id == payment_id)
    res = await session.execute(stmt)
    element = res.mappings().fetchone()
    if not element:
        raise HTTPException(status_code=404, detail="Item not found")
    return element


async def insert_payment(payment_data, session: AsyncSession):
    delta = 1
    dict_data = payment_data.dict()
    dict_data["method"] = dict_data["method"].value
    stmt = db.insert(payment).values(**dict_data)
    await session.execute(stmt)
    stmt = db.select(category).where(category.c.category_id == dict_data.get("category"))
    res = await session.execute(stmt)
    if res.fetchone()[2] == "spending":
        delta *= -1
    await update_wallet_on_insert(delta * dict_data["amount"], dict_data["owner"], session)
    await session.commit()
    return JSONResponse(content={"detail": "done"}, status_code=201)


async def update_wallet_on_insert(delta, owner_id, session: AsyncSession):
    stmt = db.select(user).where(user.c.id == owner_id)
    res = await session.execute(stmt)
    old_value = res.fetchone()[-1]
    stmt = db.update(user).where(user.c.id == owner_id).values(wallet=old_value + delta)
    await session.execute(stmt)

