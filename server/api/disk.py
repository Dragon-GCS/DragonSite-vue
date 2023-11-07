import asyncio
from hashlib import md5
from io import BytesIO
from typing import List
from uuid import UUID

from aiofiles import open
from fastapi import APIRouter, Body, Depends, Query, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from PIL import Image
from typing_extensions import Annotated

from server.config import FILE_DIR, THUMBNAIL_SIZE, FileTypeEnum
from server.depends import load_user_data
from server.exceptions import InvalidRequest, ResourceAlreadyExists, ResourceNotFound
from server.models import FileInfo, UserData
from server.schemas import Resource

router = APIRouter(prefix="/disk", tags=["disk"])


@router.get("/resources", response_model=list[Resource])
async def get_resources(
    parent: Annotated[UserData, Depends(load_user_data)],
    category: Annotated[
        FileTypeEnum, Query(description="Filter resources by category")
    ] = FileTypeEnum.NONE,
):
    filter_ = {"parent": parent, "owner": parent.owner}
    if category != FileTypeEnum.NONE:
        filter_["meta__category"] = category
    return await UserData.objects.filter(**filter_).select_related(["meta", "parent"]).all()


@router.get("/download")
async def download_file(
    resource: Annotated[UserData, Depends(load_user_data)],
    preview: bool = Query(False, description="Will return a stream response"),
    thumbnail: bool = Query(False, description="Whether return low resolution img"),
):
    await resource.load_all(exclude=["parent", "owner"])
    assert resource.meta, f"Resource({resource}) without meta"
    mime_type = resource.meta.mime_type
    if resource.meta.category == FileTypeEnum.IMAGE and thumbnail:
        buffer = BytesIO()
        Image.open(resource.real_path).resize(THUMBNAIL_SIZE).save(buffer, mime_type.split("/")[-1])
        buffer.seek(0)
        return StreamingResponse(
            buffer, media_type=mime_type, headers={"Content-Length": str(len(buffer.getvalue()))}
        )

    if preview:

        async def load():
            async with open(resource.real_path, "rb") as f:
                async for line in f:
                    yield line

        return StreamingResponse(
            load(), media_type=mime_type, headers={"Content-Length": str(resource.meta.size)}
        )

    return FileResponse(resource.real_path, media_type=mime_type, filename=str(resource.name))


@router.post(
    "/resources", summary="Create a folder under the specified path", response_model=list[Resource]
)
async def create_resource(
    folder: Annotated[UserData, Depends(load_user_data)],
    name: Annotated[str | None, Query()] = None,
    files: Annotated[List[UploadFile] | None, UploadFile] = None,
):
    if name and files:
        raise InvalidRequest("Cannot create folder and file at the same time")

    if name is not None:
        if await UserData.objects.filter(name=name, owner=folder.owner, is_dir=True).exists():
            raise ResourceAlreadyExists(name)

        folder = await UserData(name=name, owner=folder.owner, parent=folder, is_dir=True).save()
        return [folder]

    if not files:
        raise InvalidRequest("No files or fold to create")

    new_resources = []
    for file in files:
        if await UserData.objects.filter(
            name=file.filename, parent=folder, owner=folder.owner
        ).exists():
            continue

        content = await file.read()
        meta = FileInfo(
            digest=md5(content).hexdigest(),
            category=FileTypeEnum.sort_by_mime(file.content_type),
            mime_type=file.content_type,
            size=len(content),
        )

        if not await FileInfo.objects.filter(digest=meta.digest).exists():
            async with open(FILE_DIR / meta.digest, "wb") as f:
                await asyncio.gather(f.write(content), meta.save())

        new_resources.append(
            UserData(
                name=file.filename,
                owner=folder.owner,
                parent=folder,
                is_dir=False,
                meta=meta,
            )
        )
    if new_resources:
        await UserData.objects.bulk_create(new_resources)
    return new_resources


@router.delete(
    "/resources", summary="Delete the resources under specified path", response_model=list[Resource]
)
async def delete_resources(
    folder: Annotated[UserData, Depends(load_user_data)],
    names: List[str] = Query(description="Resources' name to delete under path"),
):
    """Remove resource with specified path and owner."""
    resources = (
        await UserData.objects.prefetch_related("meta")
        .filter(parent=folder, owner=folder.owner)
        .all()
    )
    await UserData.objects.delete(name__in=names, owner=folder.owner, parent=folder)
    return list(filter(lambda r: r.name not in names, resources))


@router.patch(
    "/resources",
    summary="Rename resource or move resources",
    response_model=List[Resource],
)
async def modify_resource(
    target: Annotated[UserData, Depends(load_user_data)],
    src: Annotated[list[UUID], Body(description="Resources' to be moved")],
    names: Annotated[
        List[str],
        Body(
            description=("Resources' name after rename"),
        ),
    ],
) -> List[UserData]:
    if len(src) != len(names):
        raise InvalidRequest("The length of path and name should be equal")
    resources = {
        resource.id: resource
        for resource in await UserData.objects.prefetch_related(["meta", "parent"]).all(
            id__in=src, owner=target.owner
        )
    }
    if missing_resources := set(src) - set(resources):
        raise ResourceNotFound(", ".join(resources[_id].name for _id in missing_resources))

    for _id, name in zip(src, names):
        if resources[_id].name == "/":
            raise InvalidRequest("Cannot rename the root folder")
        resources[_id].name = name
        resources[_id].parent = target

    to_update = list(resources.values())
    await UserData.objects.bulk_update(to_update, columns=["name", "parent"])
    return to_update
