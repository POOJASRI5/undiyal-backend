from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float
from database import Base


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
    merchant_name = Column(String)
    invoice_date = Column(String)

    payment_mode = Column(String)
    paid_status = Column(String)

    notes = Column(String)
    source = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    monthly_budget = Column(Float)
