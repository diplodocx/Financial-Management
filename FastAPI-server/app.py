from fastapi import FastAPI, Depends

from src.auth.auth import auth_backend
from src.auth.models import User
from src.auth.routers import fastapi_users
from src.auth.schemas import UserRead, UserCreate

app = FastAPI(title="kanban app")

current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)