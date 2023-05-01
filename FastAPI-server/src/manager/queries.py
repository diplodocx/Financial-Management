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
    res = await validate_owner(dict_data["owner"], session)
    if not res:
        raise ValueError("No such user")
    res = await validate_category(dict_data["category"], session)
    if not res:
        raise ValueError("No such category")
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


async def validate_owner(owner_id, session: AsyncSession):
    stmt = db.select(user).where(user.c.id == owner_id)
    res = await session.execute(stmt)
    return res.fetchone()


async def validate_category(category_id, session: AsyncSession):
    stmt = db.select(category).where(category.c.category_id == category_id)
    res = await session.execute(stmt)
    return res.fetchone()


async def delete_payment(payment_id, session: AsyncSession):
    delta = 1
    stmt = db.select(category).join(payment, payment.c.category == category.c.category_id) \
        .where(payment.c.payment_id == payment_id)
    res = await session.execute(stmt)
    element = res.fetchone()
    if not element:
        raise HTTPException(status_code=404, detail="Item not found")
    if element[2] == "spending":
        delta *= -1
    stmt = db.select(user, payment.c.amount).join(payment, user.c.id == payment.c.owner) \
        .where(payment.c.payment_id == payment_id)
    res = await session.execute(stmt)
    element = res.fetchone()
    owner_id = element[0]
    await update_wallet_on_delete(delta * element[-1], owner_id, session)
    stmt = payment.delete().where(payment.c.payment_id == payment_id)
    await session.execute(stmt)
    await session.commit()


async def update_wallet_on_delete(delta, owner_id, session: AsyncSession):
    stmt = db.select(user).where(user.c.id == owner_id)
    res = await session.execute(stmt)
    old_value = res.fetchone()[-1]
    stmt = db.update(user).where(user.c.id == owner_id).values(wallet=old_value - delta)
    await session.execute(stmt)


async def select_user_info(user_id, session: AsyncSession):
    stmt = db.select(user).where(user.c.id == user_id)
    res = await session.execute(stmt)
    return res.mappings().fetchone()
