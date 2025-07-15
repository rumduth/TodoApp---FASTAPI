from fastapi import APIRouter, HTTPException
from dependency import db_dependency, user_dependency, hashing_password, validate_password
from starlette import status
from models import Users
from pydantic import BaseModel, Field
router = APIRouter(
    prefix="/user",
    tags=['users']
)


class PasswordModel(BaseModel):
    password: str
    new_password: str = Field(
        min_length=6, description="Password must have length at least 6")


class PhoneModel(BaseModel):
    phone_number: str
    new_phone_number: str = Field(
        min_length=9, description="You must provide your new phone number")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(401, "User is not authenticated")
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, password_model: PasswordModel):
    if not user:
        raise HTTPException(401, "User is not authenticated")
    current_user = db.query(Users).filter(Users.id == user.get("id")).first()
    if not validate_password(password_model.password, current_user.hashed_password):
        raise HTTPException(
            401, "Error on password change")
    current_user.hashed_password = hashing_password(
        password_model.new_password)
    db.add(current_user)
    db.commit()


@router.put("/change-phone-number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_model: PhoneModel):
    if not user:
        raise HTTPException(401, "User is not authenticated")
    current_user = db.query(Users).filter(Users.id == user.get("id")).first()
    if current_user.phone_number != phone_model.phone_number:
        raise HTTPException(
            401, "Error on phone number change")
    current_user.phone_number = phone_model.new_phone_number
    db.add(current_user)
    db.commit()
