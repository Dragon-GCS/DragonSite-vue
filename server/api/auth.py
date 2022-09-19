import time

from fastapi import APIRouter, Form, Response
from server.config import COOKIE_MAX_AGE
from server.exceptions import AuthError
from server.models.user import User
from server.utils import create_token

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login")
async def login(response: Response, username: str = Form(), password: str = Form()):
    user = await User.objects.get_or_none(username=username)
    if not user:
        raise AuthError("User not found")
    if not user.validate_password(password):
        raise AuthError()
    expired_time = int(time.time() + COOKIE_MAX_AGE)
    token = create_token(user.password, expired_time)
    # response.set_cookie(key="username", value=username, max_age=COOKIE_MAX_AGE)
    # response.set_cookie(key="expired_time",
    #                     value=str(expired_time),
    #                     max_age=COOKIE_MAX_AGE)
    # print(expired_time)
    return {"username": user.username, "token": token, "expired_time": expired_time}


@router.post("/logout")
async def logout(response: Response):
    # response.delete_cookie(key="username")
    # response.delete_cookie(key="expired_time")
    return {"message": "logout"}
