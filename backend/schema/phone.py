from pydantic import BaseModel


class PhoneCreate(BaseModel):
    contact_id: int
    phone: str



class PhoneUpdate(BaseModel):
    phone: str | None = None


# For sending phone data in response
class PhoneResponse(BaseModel):
    phone_id: int
    contact_id: int
    phone: str

    class Config:
        from_attributes = True