from datetime import date
from pydantic import BaseModel, ConfigDict


class InvoiceFileResponse(BaseModel):
    id: int
    invoice_id: int
    file_name: str
    file_type: str
    file_path: str
    uploaded_date: date | None

    model_config = ConfigDict(from_attributes=True)