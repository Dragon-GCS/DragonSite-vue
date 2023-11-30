import time
from typing import Annotated

from fastapi import APIRouter, Form, Response

from server.config import COOKIE_MAX_AGE
from server.exceptions import InvalidLogin
from server.models import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login")
async def login(
    response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    user = await User.objects.get_or_none(username=username)
    if not (user and user.validate_password(password)):
        raise InvalidLogin()
    expired_time = int(time.time() + COOKIE_MAX_AGE)
    token = user.generate_token(expired_time)
    response.set_cookie(key="username", value=username, max_age=COOKIE_MAX_AGE)
    response.set_cookie(key="token", value=token, max_age=COOKIE_MAX_AGE)
    response.set_cookie(key="expired_time", value=str(expired_time), max_age=COOKIE_MAX_AGE)
    return {"message": "login"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "logout"}
