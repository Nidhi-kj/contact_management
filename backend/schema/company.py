
from pydantic import BaseModel, ConfigDict
from typing import Optional


class CompanyCreate(BaseModel):
    contact_id: int
    name: str
    website: str
    phone: str


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None


class CompanyResponse(BaseModel):
    company_id: int
    name: str
    website: str
    phone: str

    model_config = ConfigDict(from_attributes=True)
