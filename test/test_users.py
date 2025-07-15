from .utils import *

from dependency import get_current_user, get_db, validate_password
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("username") == "duthng98"
    assert response.json().get("email") == "duthng98@gmail.com"
    assert response.json().get("first_name") == 'Thong'
    assert response.json().get("last_name") == "Nguyen"
    assert response.json().get("role") == "admin"
    assert response.json().get("phone_number") == "123456789"


def test_change_password_success(test_user):
    request = {
        "password": "123456",
        "new_password": "1234567"
    }
    response = client.post("/user/change-password", json=request)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.id == 1).first()
    assert validate_password("1234567", user.hashed_password) is True


def test_change_invalid_password(test_user):
    request = {
        "password": "1234565",
        "new_password": "1234567"
    }
    response = client.post("/user/change-password", json=request)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_user):
    request = {
        "phone_number": "123456789",
        "new_phone_number": "123456777"
    }
    response = client.put("/user/change-phone-number", json=request)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.id == 1).first()
    assert user.phone_number == "123456777"
