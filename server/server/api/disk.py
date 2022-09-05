from hashlib import md5
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from pydantic import BaseModel
from server.config import FILE_PATH_REGEX, FILENAME_REGEX, FileCats
from server.models import UserData

router = APIRouter(prefix="/disk", tags=["disk"])


@router.get("/",
            summary="Get the resources under the specified path",
            response_model=List[UserData],
            response_model_exclude={"id", "parent"})
async def get_resources(path: str = Query(regex=FILE_PATH_REGEX),
                        category: FileCats = Query(
                            FileCats.ALL, description="Filter resources by category")):
    return await UserData.get_resources(path, category)


@router.post("/",
             summary="Create a folder under the specified path",
             response_model=List[UserData],
             response_model_exclude={"id", "parent"})
async def add_resource(path: str = Query(regex=FILE_PATH_REGEX),
                       name: List[str] = Query(regex=FILENAME_REGEX)):
    are_dir = [True] * len(name)
    files_size = [0] * len(name)
    mime_type = digests = [""] * len(name)
    return await UserData.create_resources(path, name, are_dir, files_size, mime_type,
                                           digests)


@router.post("/upload",
             summary="Upload files to the specified path",
             response_model=List[UserData],
             response_model_exclude={"id", "parent"})
async def upload_resource(path: str = Query(regex=FILE_PATH_REGEX),
                          files: List[UploadFile] = File()):

    are_dir = [False] * len(files)
    names, files_size, mime_type, digests = [], [], [], []
    for file in files:
        names.append(file.filename)
        mime_type.append(file.content_type)
        content = await file.read()
        files_size.append(len(content))
        digests.append(md5(content).hexdigest())
    print(names, files_size, mime_type, digests)
    return await UserData.create_resources(path, names, are_dir, files_size, mime_type,
                                           digests)


@router.delete("/", summary="Delete the resources under specified path")
async def delete_resources(
        path: str = Query(regex=FILE_PATH_REGEX),
        is_dir: List[bool] = Query(
            description="Whether resource is a dir, same order as the names"),
        name: List[str] = Query(description="Resources' name to delete under path")):
    if path == "/":
        path = ""
    paths = [f"{path}/{n}" for n in name]
    return await UserData.remove_resources(paths, is_dir)


@router.patch("/",
              summary="Rename resource or move resources",
              response_model=List[UserData],
              response_model_exclude={"id", "parent"})
async def modify_resource(path: str = Query(regex=FILE_PATH_REGEX),
                    target: str = Query(regex=FILE_PATH_REGEX),
                    is_dir: List[bool] = Query(
                        default=[], description="Resource to be rename/move is a dir or not"),
                    names: List[str] = Query(
                        default=[],
                        description=("When names is empty, rename path to target, "
                                     "otherwise move these resources to target"))):
    if names:
        return await UserData.move_resources(path, target, names, is_dir)
    # use the last part of target split by '/' as new name
    new_name = target.rsplit("/", 1)[-1]
    return await UserData.rename_resource(path, new_name, is_dir[0])
