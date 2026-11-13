# API se aane wale data ko validate (check) karna aur API response ka structure define karna.

from pydantic import BaseModel
from typing import Optional


class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str
    company_id: Optional[int] = None


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company_id: Optional[int] = None
