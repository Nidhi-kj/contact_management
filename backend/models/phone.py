from sqlalchemy import Column, String, Integer, ForeignKey
from main.database import Base


class Phone(Base):
    __tablename__ = "phone"

    phone_id = Column(Integer, primary_key=True, index=True)

    contact_id = Column(Integer, ForeignKey("contacts.contact_id"), nullable=False)

    phone = Column(String(15), nullable=False)

