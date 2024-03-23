from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app import crud

from app.api import dependencies as deps

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_enrollee(db, email: str, password: str):
    enrollee = crud.enrollee.get_by_email(db=db, email=email)
    if not enrollee:
        return False
    if not verify_password(password, enrollee.password):
        return False
    return enrollee


def authenticate_employee(db, email: str, password: str):
    employee = crud.employee.get_by_email(db=db, email=email)
    if not employee:
        return False
    if not verify_password(password, employee.password):
        return False
    return employee


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_enrollee(request: Request, db=Depends(deps.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if request.cookies.get("token") is None:
            return None
        payload = jwt.decode(
            request.cookies.get("token"), SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    enrollee = crud.enrollee.get_by_email(db=db, email=email)
    if enrollee is None:
        return None
    return enrollee


def get_current_employee(request: Request, db=Depends(deps.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if request.cookies.get("token") is None:
            return None
        payload = jwt.decode(
            request.cookies.get("token"), SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    employee = crud.employee.get_by_email(db=db, email=email)
    if employee is None:
        return None
    return employee
