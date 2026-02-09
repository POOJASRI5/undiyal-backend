from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    college: str
    city: str
    state: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class ExpenseCreate(BaseModel):
    user_email: str
    amount: float
    category: str
    merchant_name: str
    invoice_date: str
    payment_mode: str
    paid_status: str
    notes: str
    source: str
