from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from models import Users
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from dependency import db_dependency, SECRET_KEY, ALGORITHM, hashing_password, authenticate_user, create_access_token
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


class CreateUserRequest(BaseModel):
    email: str = Field(min_length=3)
    username: str = Field(min_length=3)
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str = Field(min_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str


templates = Jinja2Templates(directory="templates")

### Pages ###


@router.get("/login-page")
async def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
async def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

### Endpoints ###


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=hashing_password(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    print(create_user_request)
    try:
        db.add(create_user_model)
        db.commit()
    except:
        raise HTTPException(status_code=401, detail="User is already created")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=30))
    return {
        'access_token': token, 'token_type': "bearer"
    }
