from .utils import *
from fastapi import HTTPException
from dependency import get_current_user, get_db, authenticate_user, create_access_token, ALGORITHM, SECRET_KEY
from datetime import timedelta
import jwt
import pytest
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "123456", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("Wrong user name", "1234567", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "12345677", db)
    assert wrong_password_user is False


def test_create_access_token(test_user):
    db = TestingSessionLocal()
    token = create_access_token(
        test_user.username, test_user.id, test_user.role, timedelta(minutes=30), )
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token['sub'] == test_user.username
    assert decoded_token['id'] == test_user.id
    assert decoded_token['role'] == test_user.role
    db.close()


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {"username": 'testuser', 'id': 1, "role": 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate user."
