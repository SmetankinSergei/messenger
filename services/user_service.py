from config import SECRET_KEY, ALGORITHM
from repositories import user_repo
from schemas.models import UserCreate, UserOut
from security import hash_password

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from models.user import User
from schemas.token import Token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(user_data: UserCreate, db: Session) -> UserOut:
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pw,
    )
    saved_user = user_repo.save_user(db, new_user)
    return UserOut.from_orm(saved_user)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def login_user(form_data: OAuth2PasswordRequestForm, db: Session) -> Token:
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")
