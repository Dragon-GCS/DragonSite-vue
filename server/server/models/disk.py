from datetime import datetime
from typing import Any, ForwardRef, List, Optional

import ormar
from loguru import logger
from pydantic import validator
from server.config import FILE_DIR, FILE_PATH_REGEX, FileCats
from server.exceptions import (ArgsLengthNotEqual, FieldCheckError, ResourceNotFound,
                               RootRenameError)
from typing_extensions import Self

from .base import AutoUpdateModified, BaseConfig, BaseMeta
from .user import User


class Digest(ormar.Model):
    class Meta(BaseMeta):
        tablename = "digest"

    id: int = ormar.Integer(primary_key=True)  #  type: ignore
    digest: str = ormar.String(max_length=32, unique=True)  # type: ignore

    @validator("digest")
    def check_digest(cls, digest):
        if len(digest) != 32:
            raise ValueError("digest length must be 32")
        return digest


Parent = ForwardRef("UserData")


class UserData(ormar.Model):
    """User data model.
    Args:
        path: full path of the file or directory.
        is_dir: whether the file is a directory.
        category: file category, enum in FileCats.
        mime_type: file mime type.
        file_size: file size or directory size.
        digest: file digest.
        owner: user who owns the file.
        parent: parent UserData of the file, only '/' is root.
    """
    class Meta(BaseMeta):
        tablename = "user_data"
        queryset_class = AutoUpdateModified

    class Config(BaseConfig):
        ...

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    path: str = ormar.String(max_length=1024, regex=FILE_PATH_REGEX)  # type: ignore
    is_dir: bool = ormar.Boolean()
    category: str = ormar.String(default=FileCats.NONE.value,
                                 max_length=20,
                                 choices=list(FileCats))  # type: ignore
    mime_type: str = ormar.String(default="", max_length=80)  # type: ignore
    create_time: datetime = ormar.DateTime(default=datetime.now)  # type: ignore
    modified_time: datetime = ormar.DateTime(default=datetime.now)  # type: ignore
    file_size: int = ormar.Integer(default=0)  # type: ignore

    digest: Optional[Digest] = ormar.ForeignKey(Digest,
                                                ondelete="CASCADE",
                                                nullable=True,
                                                related_name="files")
    owner: Optional[User] = ormar.ForeignKey(User,
                                             ondelete="CASCADE",
                                             nullable=True,
                                             related_name="data")
    parent: Optional[Parent] = ormar.ForeignKey(  # type: ignore
        Parent, ondelete="CASCADE", related_name="children")

    @ormar.property_field
    def name(self) -> str:
        if not self.path:
            return ""
        if self.path == "/":
            return "root"
        return self.path.rsplit("/", 1)[-1]

    @ormar.property_field
    def parent_path(self) -> Optional[str]:
        if not self.path:
            return
        if self.path.count("/") == 1:
            return "/"
        return self.path.rsplit("/", 1)[0]

    def human_size(self, fmt: str = "M") -> str:
        if fmt == "K":
            return f"{self.file_size / 1024:.2f}Kb"
        if fmt == "M":
            return f"{self.file_size / 1024 / 1024:.2f}Mb"
        if fmt == "G":
            return f"{self.file_size / 1024 / 1024 / 1024:.2f}Gb"
        return f"{self.file_size}B"

    def get_real_path(self):
        """Get the real path which store this resource"""
        if not self.digest:
            raise ValueError("Only files has real path")
        return FILE_DIR / self.digest.digest

    async def update(self, _columns: List[str] = [], **kwargs: Any) -> Self:
        self.modified_time = datetime.now()
        return await super().update(_columns, **kwargs)

    @classmethod
    async def create_resources(cls,
                               path: str,
                               names: List[str],
                               are_dir: List[bool],
                               files_size: List[int] = [0],
                               mime_types: List[str] = [""],
                               digests: List[str] = [""],
                               user: Optional[User] = None) -> List[Self]:
        """Create user's resources under specified path with name, is_dir, file_size, mime_type, digest.

        Args:
            path: Folder path of the resources.
            names: The list of names of the resources.
            is_dir: The list of whether the resources are directories.
            files_size: The list of file sizes of the resources, dir's size is 0.
            mime_types: The list of mime types of the resources, dir's type is "".
            digests: The list of digests of the resources, dir's digest is "".
            user: The owner of the resources.
        Returns:
            The list of created resources.
        """
        if not (len(names) == len(are_dir) == len(files_size) == len(mime_types) ==
                len(digests)):
            raise ArgsLengthNotEqual(
                ["name", "is_dir", "file_size", "mime_type", "digest"],
                [names, are_dir, files_size, mime_types, digests])

        if not all(names):
            raise FieldCheckError("UserData.name", names)

        parent = await cls.objects.get_or_none(path=path, is_dir=True, owner=user)
        if not parent:
            raise ResourceNotFound(path)

        if path == "/":
            path = ""

        resources: List[UserData] = []
        creates: List[UserData] = []
        for name, is_dir, file_size, mime_type, digest in zip(names, are_dir, files_size,
                                                              mime_types, digests):
            if not is_dir and not all((file_size, mime_type, digest)):
                logger.debug(
                    f"File<{name}>'s size[{file_size}], mime_type[{mime_type}], digest[{digest}] cannot be empty."
                )
                continue

            if is_dir:
                file_size, mime_type, digest = 0, "", None
            else:
                digest, _ = await Digest.objects.get_or_create(digest=digest)

            resource_path = f"{path}/{name}"
            # load parent model to avoid field check error in response
            resource = await cls.objects.select_related("parent").get_or_none(
                path=resource_path, is_dir=is_dir, owner=user)

            if resource is not None:
                parent.file_size += resource.file_size
                logger.info(f"Resource<{path}/{name}> already exists.")
            else:
                parent.file_size += file_size
                resource = UserData(path=resource_path,
                                    is_dir=is_dir,
                                    category=FileCats.sort_mime_type(mime_type),
                                    mime_type=mime_type,
                                    file_size=file_size,
                                    digest=digest,
                                    owner=user,
                                    parent=parent)
                creates.append(resource)
            resources.append(resource)
        if creates:
            await cls.objects.bulk_create(creates)
            logger.success(f"Created resources{[r.path for r in creates]}.")
        await parent.update()  # update modified_time
        logger.debug(resources)
        return resources

    @classmethod
    async def get_resources(cls,
                            path: str,
                            category: FileCats = FileCats.ALL,
                            owner: Optional[User] = None) -> List[Self]:
        """Get resource with specified path and owner."""
        parent = await cls.objects.get_or_none(path=path, owner=owner)
        if not parent:
            raise ResourceNotFound(path)
        filters = cls.objects.select_related("parent").filter(parent=parent, owner=owner)
        if category != FileCats.ALL:
            filters = filters.filter(category=category.value)
        return await filters.all()

    @classmethod
    async def remove_resources(cls,
                               paths: List[str],
                               are_dir: List[bool],
                               owner: Optional[User] = None):
        """Remove resource with specified path and owner."""
        if len(paths) != len(are_dir):
            raise ArgsLengthNotEqual(["path", "is_dir"], [paths, are_dir])

        for path, is_dir in zip(paths, are_dir):
            resource = await cls.objects.get_or_none(path=path,
                                                     is_dir=is_dir,
                                                     owner=owner)
            if not resource:
                continue
            await resource.delete()
            logger.success(f"Resource<{path}> removed.")

    @classmethod
    async def rename_resource(cls,
                              path: str,
                              new_name: str,
                              is_dir: bool,
                              owner: Optional[User] = None) -> Self:
        """Rename resource with specified path and owner."""
        if not new_name:
            raise FieldCheckError("UserData.name", new_name)

        if path == "/":
            raise RootRenameError()

        resource = await cls.objects.get_or_none(path=path, is_dir=is_dir, owner=owner)
        if not resource:
            raise ResourceNotFound(path)

        parent = resource.parent_path
        new_path = f"{parent if parent != '/' else ''}/{new_name}"

        if resource.is_dir:
            resource.path = new_path
            sub_resources = [resource]
            for r in await cls.objects.filter(path__startswith=path + "/",
                                              owner=owner).all():
                r.path = new_path + r.path[len(path):]
                sub_resources.append(r)
            await cls.objects.bulk_update(sub_resources)
        else:
            await resource.update(path=new_path)
        logger.success(f"Rename resource <{path}> to {resource.path}.")
        return resource

    @classmethod
    async def move_resources(cls,
                             src_path: str,
                             dst_path: str,
                             names: List[str],
                             are_dir: List[bool],
                             owner: Optional[User] = None) -> List[Self]:
        """Move src to dst when names was not given, otherwise move name form src to dst"""
        if len(names) != len(are_dir):
            raise ArgsLengthNotEqual(["name", "is_dir"], [names, are_dir])

        src = await cls.objects.get_or_none(path=src_path, is_dir=True, owner=owner)
        dst = await cls.objects.get_or_none(path=dst_path, is_dir=True, owner=owner)
        if not dst or not src:
            raise ResourceNotFound(dst_path if not dst else src_path)

        if dst_path == "/":
            dst_path = ""
        if src_path == "/":
            src_path = ""

        resources = []
        for name, is_dir in zip(names, are_dir):
            resource = await cls.objects.get_or_none(path=f"{src_path}/{name}",
                                                     is_dir=is_dir,
                                                     owner=owner)
            if not resource:
                continue
            dst_resource = await cls.objects.get_or_none(path=f"{dst_path}/{name}",
                                                         is_dir=is_dir,
                                                         owner=owner)
            if dst_resource:
                resources.append(dst_resource)
                continue
            resource.parent = dst
            resource.path = f"{dst_path}/{name}"
            resources.append(resource)

        if not resources:
            return []
        await cls.objects.bulk_update(resources, ["parent", "path", "modified_time"])
        logger.success(
            f"Moving resources{[r.name for r in resources]} from {src.path} to {dst.path}."
        )
        return resources


UserData.update_forward_refs()
