from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    college = Column(String)
    city = Column(String)
    state = Column(String)

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    amount = Column(Float)
    category = Column(String)
    source = Column(String)  # SMS / OCR / MANUAL
    created_at = Column(DateTime, default=datetime.utcnow)
