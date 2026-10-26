from datetime import date
from sqlalchemy import Boolean, Date, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key= True,
        index =True
        )

    username: Mapped[str] = mapped_column(
        String(50),
        unique =True, 
        nullable = False
    )

    email: Mapped[str] = mapped_column(
        String(200),
        unique = True, 
        nullable = False, 
        index = True
    )


    password: Mapped[str] = mapped_column(
        String(250), 
        nullable = False
    )

    role: Mapped[str] = mapped_column(
        String(20), 
        nullable =  False, 
        default =  "employee"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable= False, 
        default= True
    )

    created_at: Mapped[date] = mapped_column(
        Date,
        nullable = False,
        server_default = func.current_date()
    )
