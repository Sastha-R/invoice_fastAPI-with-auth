from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_models import User


class UserRepository:

    async def create(self, db: AsyncSession, user_data: dict) -> User:
        user = User(**user_data)

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> User | None:
        statement = select(User).where(User.email == email)

        result = await db.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id(
        self, db: AsyncSession, user_id: int
    ) -> User | None:
        statement = select(User).where(User.id == user_id)

        result = await db.execute(statement)

        return result.scalar_one_or_none()
