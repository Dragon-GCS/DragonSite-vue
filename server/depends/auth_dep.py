import time
from typing import Annotated, Optional

from fastapi import Cookie

from server.exceptions import InvalidLogin
from server.models import User


async def get_user(
    personal: bool = False,
    token: Annotated[str, Cookie()] = "",
    username: Annotated[str, Cookie()] = "",
    expired_time: Annotated[int, Cookie()] = 0,
) -> Optional[User]:
    if not personal:
        return
    if int(time.time()) > expired_time:
        raise InvalidLogin("Authentication expired")
    if not token:
        raise InvalidLogin("Token is required")
    user = await User.objects.get_or_none(username=username)
    if not user:
        raise InvalidLogin("User not found")
    if not user.validate_token(token, expired_time):
        raise InvalidLogin()
    return user
