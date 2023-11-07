import sqlalchemy
from loguru import logger

from server.config import DATABASE_URL
from server.exceptions import ResourceNotFound

from .base import database, metadata  # noqa: F401
from .disk import FileInfo, UserData  # noqa: F401
from .user import User


async def init_db():
    """Initialize the database."""

    connect_args = {}
    if DATABASE_URL.startswith("sqlite"):
        import sqlite3
        import uuid

        sqlite3.register_adapter(uuid.UUID, lambda u: u.hex)
        connect_args["check_same_thread"] = False

    engine = sqlalchemy.create_engine(DATABASE_URL, connect_args=connect_args)
    metadata.create_all(engine)
    await UserData.objects.get_or_create(name="/", is_dir=True, owner=None)
    logger.info("Initialized database: " + DATABASE_URL)


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

    user = await User.objects.get_or_none(username=username)
    if user is None:
        user = User(username=username, password=password, is_admin=is_admin)
        await UserData(name="/", is_dir=True, owner=user).save_related()
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
