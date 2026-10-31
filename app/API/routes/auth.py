from fastapi import (
            APIRouter,
            Depends,
            status,
            Body
            )
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.API.dependencies.auth_dependency import required_admin
from app.API.dependencies.dependency import get_auth_service
from app.schemas.auth_schema import (
                    UserCreate, 
                    UserResponse,
                    UserLogin,
                    RefreshTokenRequest
                    )
from fastapi.security import OAuth2PasswordRequestForm
from app.services.implementations.auth_service import AuthService


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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login_with_form(
        db,
        form_data.username,
        form_data.password
    )


@auth_router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
    current_user=Depends(required_admin)
):
    return await auth_service.get_all_users(db)



@auth_router.post("/refresh")
async def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.refresh_access_token(
        db,
        token_data.refresh_token
    )