from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from src.auth.auth import auth_backend
from src.auth.models import User
from src.auth.routers import fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.manager.routers import manager
from src.reports.routers import reports

app = FastAPI(title="kanban app")

current_user = fastapi_users.current_user()

app.include_router(manager)
app.include_router(reports)
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

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(status_code=400, content={"msg": str(exc)})