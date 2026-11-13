# YHA MODEL BNAYA H Database table ka structure define karta hai

from sqlalchemy import Column, String, Integer, ForeignKey
from main.database import Base



class Contact(Base):
    __tablename__ = "contacts"

    contact_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=True)

    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    


