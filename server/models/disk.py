import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import ForwardRef, Optional, Type

import ormar
from loguru import logger

from server.config import FILE_DIR, FileTypeEnum
from server.exceptions import InvalidRequest

from .base import BaseMeta
from .user import User

# regex for validating file name
FILENAME_REGEX = r'[^/\<>:*|?."]|^/$'


class FileInfo(ormar.Model):
    """Model representing file information.

    Attributes:
        digest (str): The digest of the file, which is the primary key.
        mime_type (str): The MIME type of the file.
        create_time (datetime): The creation time of the file.
        file_size (int): The size of the file in bytes.
        category (FileTypeEnum): The category of the file.
    """

    class Meta(BaseMeta):
        tablename = "digest"

    digest: str = ormar.String(min_length=32, max_length=32, primary_key=True)  # type: ignore
    mime_type: str = ormar.String(max_length=80)  # type: ignore
    create_time: datetime = ormar.DateTime(default=datetime.now)  # type: ignore
    size: int = ormar.Integer(default=0)  # type: ignore
    category: FileTypeEnum = ormar.Enum(enum_class=FileTypeEnum, default=FileTypeEnum.NONE)


Parent = ForwardRef("UserData")


class UserData(ormar.Model):
    """User data model.

    Args:
        name: name of the file or directory.
        is_dir: whether the file is a directory.
        modified_time: last modified time of the data.
        meta: file information.
        owner: user who owns the file.
        parent: parent UserData of the file, only '/' is root.
    """

    class Meta(BaseMeta):
        tablename = "user_data"
        constraints = [ormar.IndexColumns("owner", "parent", "is_dir", "name", unique=True)]

    id: uuid.UUID = ormar.UUID(default=uuid.uuid4, primary_key=True)  # type: ignore
    name: str = ormar.String(max_length=4096, regex=FILENAME_REGEX)  # type: ignore
    is_dir: bool = ormar.Boolean()
    modified_time: datetime = ormar.DateTime(default=datetime.now)  # type: ignore

    meta: Optional[FileInfo] = ormar.ForeignKey(
        FileInfo, ondelete="CASCADE", nullable=True, related_name="files"
    )
    owner: Optional[User] = ormar.ForeignKey(
        User, ondelete="CASCADE", nullable=True, related_name="data"
    )
    parent: Optional[Parent] = ormar.ForeignKey(  # type: ignore
        Parent, ondelete="CASCADE", related_name="children"
    )

    @property
    def real_path(self) -> Path:
        """Get the real path which store this resource"""
        assert not self.is_dir and self.meta, "Only file can attach meta"
        return FILE_DIR / self.meta.digest

    def __str__(self) -> str:
        return f"{self.name}(id='{self.id.hex}', owner='{self.owner.id if self.owner else ''}')"


UserData.update_forward_refs()


@ormar.pre_save(UserData)
async def check_owner(sender: Type[UserData], instance: UserData, **kwargs):
    """Check that the owner of the file is the same as the parent directory."""
    if instance.parent and instance.parent.owner != instance.owner:
        raise InvalidRequest("Owner of the file is not the same as the parent directory.")


@ormar.pre_update(UserData)
async def update_modified_time(sender: Type[UserData], instance: UserData, **kwargs):
    instance.modified_time = datetime.now()


@ormar.post_delete(UserData)
async def remove_file_info(sender: Type[UserData], instance: UserData, **kwargs):
    """当所有文件都被删除后，删除对应的file_info数据"""
    if not instance.meta:
        return
    if not await sender.objects.filter(meta=instance.meta).exists():
        await instance.meta.delete()
        logger.info(f"Removed meta<{instance.meta.digest}>.")


@ormar.post_delete(FileInfo)
async def remove_file(sender: Type[FileInfo], instance: FileInfo, **kwargs):
    os.remove(FILE_DIR / instance.digest)
    logger.info(f"Removed digest<{instance.digest}>.")
