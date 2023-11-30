from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query

from server.exceptions import ResourceNotFound
from server.models import User, UserData

from .auth_dep import get_user


async def load_user_data(
    user: Annotated[User, Depends(get_user)],
    path: Annotated[
        UUID | None, Query(description="Path id to list resources or target id to operate")
    ] = None,
) -> UserData:
    """Load the model with the specified path and owner"""
    if path is None:
        resource = await UserData.objects.get_or_none(parent=None, owner=user)
    else:
        resource = await UserData.objects.get_or_none(id=path, owner=user)
    if not resource:
        raise ResourceNotFound(path.hex if path else "root")
    return resource
