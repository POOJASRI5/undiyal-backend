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
    source: str