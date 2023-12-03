from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator

from server.config import FileTypeEnum


class FileInfo(BaseModel):
    digest: str
    category: FileTypeEnum
    size: int


class Parent(BaseModel):
    id: UUID
    name: str


class Resource(BaseModel):
    id: UUID
    name: str
    is_dir: bool
    modified_time: datetime
    meta: FileInfo | None
    parent: Parent | list[Parent]
    # generated fields
    size: str = ""

    # use validator to generate fields
    @validator("size", pre=True, always=True)
    def compute_size(cls, _, values) -> str:
        if not values.get("meta"):
            return ""

        size = values["meta"].size
        for fmt in ("", "K", "M", "G"):
            if size < 1024:
                return f"{size:.2f}{fmt}b"
            size /= 1024
        return f"{size:.2f}Tb"
