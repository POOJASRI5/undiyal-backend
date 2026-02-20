from PIL import Image
import io
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from schemas import UserCreate, UserLogin
from auth import create_user, authenticate_user
from database import engine
from models import Base
from models import Expense
from schemas import ExpenseCreate
import os
from dotenv import load_dotenv 
from fastapi import UploadFile, File
from gemini_service import extract_from_image
from gemini_service import get_saving_suggestions
from models import Budget
from schemas import BudgetCreate
from models import User
from pydantic import BaseModel
from sqlalchemy import text



load_dotenv()

models.Base.metadata.create_all(bind=engine)  

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# Signup
@app.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    created_user = create_user(db, user)
    if not created_user:
        return {"message": "User already exists"}
    return {
        "message": "success",
        "user_id": created_user.id,
        "email": created_user.email
    }

# Login
@app.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        return {"message": "Invalid email or password"}

    return {
        "message": "success",
        "user_id": authenticated_user.id,
        "email": authenticated_user.email
    }

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/expenses")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(
        user_email=expense.user_email,
        amount=expense.amount,
        category=expense.category,
        merchant_name=expense.merchant_name,
        invoice_date=expense.invoice_date,
        payment_mode=expense.payment_mode,
        paid_status=expense.paid_status,
        notes=expense.notes,
        source=expense.source
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return {"message": "Expense added successfully"}

@app.post("/test-gemini")
async def test_gemini(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    result = extract_from_image(image)

    return {"result": result}



@app.get("/expenses")
def get_expenses(user_email: str, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(
        Expense.user_email == user_email
    ).all()

    return expenses


@app.post("/budget")
def set_budget(data: BudgetCreate, db: Session = Depends(get_db)):

    existing = db.query(Budget).filter(
        Budget.user_email == data.user_email
    ).first()

    if existing:
        existing.monthly_budget = data.monthly_budget
    else:
        new_budget = Budget(
            user_email=data.user_email,
            monthly_budget=data.monthly_budget
        )
        db.add(new_budget)

    db.commit()

    return {"message": "Budget saved"}

@app.get("/budget")
def get_budget(user_email: str, db: Session = Depends(get_db)):

    budget = db.query(Budget).filter(
        Budget.user_email == user_email
    ).first()

    if not budget:
        return {"monthly_budget": 0}

    return {
        "monthly_budget": budget.monthly_budget
    }

@app.get("/user/profile")
def get_user_profile(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"message": "User not found"}

    return {
        "email": user.email,
        "available_balance": user.available_balance
    }



class BalanceUpdate(BaseModel):
    email: str
    available_balance: float


@app.put("/user/balance")
def update_balance(data: BalanceUpdate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return {"message": "User not found"}

    user.available_balance = data.available_balance
    db.commit()

    return {"message": "Balance updated"}


@app.get("/ai/suggestions")
def get_ai_suggestions(user_email: str, db: Session = Depends(get_db)):

    expenses = db.query(Expense).filter(
        Expense.user_email == user_email
    ).all()

    if not expenses:
        return {"suggestions": "No expenses found yet."}

    total_spent = sum(e.amount for e in expenses)

    category_total = {}
    for e in expenses:
        category_total[e.category] = category_total.get(e.category, 0) + e.amount

    prompt = f"""
    User spending summary:

    Total spent: {total_spent}
    Category spending: {category_total}

    Give:
    1. General saving tips
    2. Personalized saving advice
    3. Beginner investment suggestions

    Keep response short and practical.
    """

    result = get_saving_suggestions(prompt)

    return {"suggestions": result}

