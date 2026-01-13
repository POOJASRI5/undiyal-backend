from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    college: str
    city: str
    state: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
