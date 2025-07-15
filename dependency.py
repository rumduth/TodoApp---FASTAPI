from typing import Annotated
from fastapi import Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
import jwt
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from models import Users
from datetime import timedelta, datetime, timezone

SECRET_KEY = "2ac39a8338895a65e6c4fe9ad2c8ddb65fcbb773e0acf4aed381255a01b05337"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def hashing_password(password: str):
    password_bytes = password.encode()
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed = hashed.decode()
    return hashed


def validate_password(password: str, hashed_passord: str):
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_passord.encode())


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None or not validate_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    payload = {
        "sub": username, "id": user_id, "exp": datetime.now(timezone.utc) + expires_delta, 'role': role
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {'username': username, 'id': user_id, "role": user_role}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
