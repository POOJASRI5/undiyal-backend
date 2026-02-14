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
import google.generativeai as genai
from dotenv import load_dotenv 
from gemini_service import model
from fastapi import UploadFile, File
from gemini_service import extract_from_image


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




