from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, db: AsyncSession, user_data: dict) -> User:
        pass

    @abstractmethod
    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> User | None:
        pass

    @abstractmethod
    async def get_by_id(
        self, db: AsyncSession, user_id: int
    ) -> User | None:
        pass

    @abstractmethod
    async def get_all(self, db: AsyncSession) -> list[User]:
        pass