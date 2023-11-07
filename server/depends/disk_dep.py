from typing import Annotated
from uuid import UUID

from fastapi import Depends, Query

from server.exceptions import ResourceNotFound
from server.models import User, UserData

from .auth_dep import get_user


async def load_user_data(
    path: Annotated[UUID, Query(description="Path id to list resources or target id to operate")],
    user: Annotated[User, Depends(get_user)],
) -> UserData:
    """Load the model with the specified path and owner"""
    resource = await UserData.objects.get_or_none(id=path, owner=user)
    if not resource:
        raise ResourceNotFound(path.hex)
    return resource
