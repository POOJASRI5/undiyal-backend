from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        return None

    new_user = models.User(
    email=user.email,
    password=hash_password(user.password),
    college=user.college,
    city=user.city,
    state=user.state,
    available_balance=user.available_balance
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
