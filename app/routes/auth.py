from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.dependency import get_auth_service
from app.schemas.auth_schemas import UserCreate, UserResponse,UserLogin

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    auth_service = Depends(get_auth_service)
):
    return await auth_service.register(db, user_data)


@auth_router.post("/login")
async def login_user(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
    auth_service = Depends(get_auth_service)
):
    return await auth_service.login(db, user_data)