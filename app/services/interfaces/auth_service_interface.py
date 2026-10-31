from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schema import UserCreate, UserLogin


class AuthServiceInterface(ABC):

    @abstractmethod
    async def register(
        self,
        db: AsyncSession,
        user_data: UserCreate
    ):
        pass

    # @abstractmethod
    # async def login(
    #     self,
    #     db: AsyncSession,
    #     user_data: UserLogin
    # ):
    #     pass

    @abstractmethod
    async def login_with_form(
        self,
        db: AsyncSession,
        email: str,
        password: str
    ):
        pass

    @abstractmethod
    async def get_all_users(self, db: AsyncSession):
        pass