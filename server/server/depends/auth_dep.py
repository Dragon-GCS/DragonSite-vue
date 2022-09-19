import time
from typing import Optional

from fastapi import Cookie, Header
from server.exceptions import AuthError
from server.models import User
from server.utils import create_token


async def get_user(
        login_require: bool,
        token: str = Header(""),
        username: str = Header(""),
        expired_time: int = Header(0, convert_underscores=False),
) -> Optional[User]:
    if not login_require:
        return
    if int(time.time()) > expired_time:
        raise AuthError("Authentication expired")
    if not token:
        raise AuthError("Token is required")
    user = await User.objects.get_or_none(username=username)
    if not user:
        raise AuthError("User not found")
    if create_token(user.password, expired_time) != token:
        raise AuthError()
    return user
