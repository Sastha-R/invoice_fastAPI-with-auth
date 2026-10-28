from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password,verify_password,create_access_token
from app.repositories.implementations.user_repository import UserRepository
from app.schemas.auth_schemas import UserCreate,UserLogin
from app.services.interfaces.auth_service_interface import AuthServiceInterface


class AuthService(AuthServiceInterface):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, db: AsyncSession, user_data: UserCreate):
        existing_user = await self.user_repository.get_by_email(
            db, user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered"
            )

        hashed_password = hash_password(user_data.password)

        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "password": hashed_password
        }

        return await self.user_repository.create(db, user_dict)

    
    async def login(self, db: AsyncSession, user_data: UserLogin):
        user = await self.user_repository.get_by_email(
            db, user_data.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        access_token = create_access_token(
        user_id=user.id,
        role=user.role
        )


        return {
        "access_token": access_token,
        "token_type": "bearer"
        }


    async def login_with_form(
            self,
            db: AsyncSession,
            email: str,
            password: str
        ):
        user = await self.user_repository.get_by_email(db, email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        access_token = create_access_token(
            user_id=user.id,
            role=user.role
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def get_all_users(self, db: AsyncSession):
        return await self.user_repository.get_all(db)
