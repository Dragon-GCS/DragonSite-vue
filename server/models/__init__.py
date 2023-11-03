from hashlib import md5

import sqlalchemy

from server.config import DATABASE_DIR, DATABASE_URL
from server.exceptions import ResourceNotFound
from server.models.base import database, metadata  # noqa: F401
from server.models.disk import UserData
from server.models.user import User


async def init_db():
    """Initialize the database."""
    if DATABASE_DIR.exists():
        return

    engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    metadata.create_all(engine)
    await UserData(path="/", is_dir=True).save()
    print("Initialized database:", DATABASE_DIR)


async def add_user(username: str, password: str, is_admin: bool = False) -> User:
    """Create a new user or change user pwd with specified username and password.

    Args:
        username: username of the new user.
        password: password of the new user, will be hashed.
        is_admin: whether the new user is an admin, only one admin is allowed.
    Returns:
        The new user.
    """
    admin = await User.objects.get_or_none(is_admin=True)
    if is_admin and admin and admin.username != username:
        raise ValueError(f"Only one admin<{admin.username}> user allowed.")

    password = md5(password.encode("utf-8")).hexdigest()
    user = await User.objects.get_or_none(username=username)
    if user is None:
        user = User(username=username, password=password, is_admin=is_admin)
        await user.save()
        await UserData(path="/", is_dir=True, owner=user).save()
    else:
        await user.update(password=password, is_admin=is_admin)

    return user


async def drop_user(username: str, password: str) -> User:
    """Drop a user with password validation

    Args:
        username: username of user to dropped
        password: password of user to dropped
    """
    user = await User.objects.get_or_none(username=username)
    if user is None:
        raise ResourceNotFound(f"User<{username}>")

    if not user.validate_password(password):
        raise ValueError(f"Password<{password}> is incorrect.")

    await user.delete()
    return user
