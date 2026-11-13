
from sqlalchemy import Column, String, Integer, ForeignKey
from main.database import Base


class Notes(Base):
    __tablename__ = "contactNotes"

    notes_id = Column(Integer, primary_key=True, index=True)

    contact_id = Column(Integer, ForeignKey("contacts.contact_id"), nullable=False)

    notes = Column(String(200))

