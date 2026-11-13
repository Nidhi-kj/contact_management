from pydantic import BaseModel


class NotesCreate(BaseModel):
    contact_id: int
    notes: str


class NotesUpdate(BaseModel):
    notes: str | None = None


class NotesResponse(BaseModel):
    notes_id: int
    contact_id: int
    notes: str

    class Config:
        from_attributes = True