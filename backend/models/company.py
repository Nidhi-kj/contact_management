# 
from sqlalchemy import Column, String, Integer, ForeignKey
from main.database import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    

    name = Column(String(100), nullable=False)
    website = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    
    