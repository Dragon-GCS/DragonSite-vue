from io import BytesIO
from hashlib import md5
from typing import Dict, List, Optional

from aiofiles import open
from fastapi import APIRouter, Depends, File, Query, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from PIL import Image
from server.config import FILE_DIR, FILE_PATH_REGEX, FILENAME_REGEX, FileCats
from server.depends import get_user
from server.exceptions import ResourceNotFound
from server.models import UserData
from server.models.disk import Digest
from server.models.user import User

router = APIRouter(prefix="/disk", tags=["disk"])

RESPONSE_EXCLUDE_FIELDS = ("id", "children", "owner", "parent")


@router.get(
    "/",
    summary="Get the resources under the specified path",
    response_model=List[UserData],
    response_model_exclude=set(RESPONSE_EXCLUDE_FIELDS),
)
async def get_resources(
    path: str = Query(regex=FILE_PATH_REGEX),
    user: Optional[User] = Depends(get_user),
    category: FileCats = Query(FileCats.ALL, description="Filter resources by category"),
) -> List[UserData]:
    return await UserData.get_resources(path, category, user)


@router.get("/download", summary="Download the specified file")
async def download_file(
    path: str = Query(regex=FILE_PATH_REGEX),
    user: Optional[User] = Depends(get_user),
    preview: bool = Query(False, description="Whether preview the file"),
    thumbnail: bool = Query(False, description="Whether return low resolution img"),
):
    resource = await UserData.objects.select_related("digest").get_or_none(path=path, owner=user)
    if not resource:
        raise ResourceNotFound(path)

    if resource.category == FileCats.IMAGE and thumbnail:
        bytes_io = BytesIO()
        Image.open(resource.get_real_path()).resize((64, 64)).save(bytes_io, "JPEG")
        return StreamingResponse(bytes_io, media_type="image/jpeg")

    if preview:

        async def load():
            async with open(resource.get_real_path(), "rb") as f:
                async for line in f:
                    yield line

        return StreamingResponse(load(), media_type=resource.mime_type)

    return FileResponse(
        resource.get_real_path(), media_type=resource.mime_type, filename=str(resource.name)
    )


@router.post(
    "/",
    summary="Create a folder under the specified path",
    response_model=List[UserData],
    response_model_exclude=set(RESPONSE_EXCLUDE_FIELDS),
)
async def create_folder(
    path: str = Query(regex=FILE_PATH_REGEX),
    user: User = Depends(get_user),
    name: List[str] = Query(regex=FILENAME_REGEX),
) -> List[UserData]:
    are_dir = [True] * len(name)
    files_size = [0] * len(name)
    mime_type = digests = [""] * len(name)
    return await UserData.create_resources(
        path, name, are_dir, files_size, mime_type, digests, user
    )


@router.post(
    "/upload",
    summary="Upload files to the specified path",
    response_model=List[UserData],
    response_model_exclude=set(RESPONSE_EXCLUDE_FIELDS),
)
async def upload_resource(
    path: str = Query(regex=FILE_PATH_REGEX),
    user: User = Depends(get_user),
    files: List[UploadFile] = File(),
) -> List[UserData]:
    are_dir = [False] * len(files)
    names, files_size, mime_type, digests = [], [], [], []
    for file in files:
        content = await file.read()
        names.append(file.filename)
        mime_type.append(file.content_type)
        files_size.append(len(content))
        digests.append(digest := md5(content).hexdigest())
        if not await Digest.check_exist(digest):
            async with open(FILE_DIR / digests[-1], "wb") as f:
                await f.write(content)
    return await UserData.create_resources(
        path, names, are_dir, files_size, mime_type, digests, user
    )


@router.delete("/", summary="Delete the resources under specified path")
async def delete_resources(
    path: str = Query(regex=FILE_PATH_REGEX),
    user: User = Depends(get_user),
    name: List[str] = Query(description="Resources' name to delete under path"),
    is_dir: List[bool] = Query(description="Whether resource is a dir, same order as the names"),
) -> Dict[str, bool]:
    if path == "/":
        path = ""
    paths = [f"{path}/{n}" for n in name]
    await UserData.remove_resources(paths, is_dir, user)
    return {"success": True}


@router.patch(
    "/",
    summary="Rename resource or move resources",
    response_model=List[UserData],
    response_model_exclude=set(RESPONSE_EXCLUDE_FIELDS),
)
async def modify_resource(
    path: str = Query(regex=FILE_PATH_REGEX),
    target: str = Query(regex=FILE_PATH_REGEX),
    user: User = Depends(get_user),
    is_dir: List[bool] = Query(
        default=[], description="Resource to be renamed/moved is a dir or not"
    ),
    names: List[str] = Query(
        default=[],
        description=(
            "When names is empty, rename path to target, "
            "otherwise move these resources to target"
        ),
    ),
) -> List[UserData]:
    if names:
        return await UserData.move_resources(path, target, names, is_dir, user)
    # use the last part of target split by '/' as new name
    new_name = target.rsplit("/", 1)[-1]
    return [await UserData.rename_resource(path, new_name, is_dir[0], user)]
