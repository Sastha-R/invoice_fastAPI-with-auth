from datetime import date
from sqlalchemy import Date, Integer, String , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice

class InvoiceFile(Base):
    __tablename__ = "invoice_files"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True
        )

    
    invoice_id : Mapped[int] = mapped_column(
        ForeignKey(
            "invoices.id", 
            ondelete="CASCADE"
            ),
        nullable=False
        )

    
    file_name : Mapped[str] = mapped_column(
        String(250), 
        nullable=False
        )

    
    file_type : Mapped[str] = mapped_column(
        String(60), 
        nullable=False
        )

    
    file_path : Mapped[str] = mapped_column(
        String(500), 
        nullable=False
        )

    
    uploaded_date : Mapped[date] =  mapped_column(
        Date, 
        nullable=True
        ) 

    
    invoice: Mapped["Invoice"] = relationship(
        back_populates="files"
        )