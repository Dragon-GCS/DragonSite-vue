from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from pydantic import BaseModel
from server.config import FILE_PATH_REGEX, FILENAME_REGEX, FileCats
from server.models import UserData

router = APIRouter(prefix="/disk", tags=["disk"])


@router.get("/", summary="Get the resources under the specified path")
async def get_resources(path: str = Query(regex=FILE_PATH_REGEX),
                        category: FileCats = Query(
                            FileCats.ALL, description="Filter resources by category")):
    files = await UserData.get_resources(path, category)
    return files
    return {"message": "get path: {path} category: {category}"}


@router.post("/", summary="Create a folder under the specified path")
async def add_resource(path: str = Query(regex=FILE_PATH_REGEX),
                       name: str = Query(regex=FILENAME_REGEX)):
    return {"message": f"add dir: {path}/{name}"}


@router.post("/upload", summary="Upload files to the specified path")
async def upload_resource(path: str = Query(regex=FILE_PATH_REGEX),
                          files: List[UploadFile] = File()):
    for file in files:
        print(file.filename)
        print(file.content_type)
        content = await file.read()
    return {
        "message": f"add {','.join('/'.join((path, file.filename)) for file in files)}"
    }


@router.delete("/", summary="Delete the resources under specified path")
async def delete_resources(
        path: str = Query(regex=FILE_PATH_REGEX),
        is_dir: List[bool] = Query(
            description="Whether resource is a dir, same order as the names"),
        names: List[str] = Query(description="Resources' name to delete under path")):
    return {
        "message":
            f"In <{path}> delete {'folder' if is_dir else 'file'} {','.join(name for name in names)}"
    }


@router.patch("/", summary="Rename resource or move resources")
def modify_resource(path: str = Query(regex=FILE_PATH_REGEX),
                    target: str = Query(regex=FILE_PATH_REGEX),
                    is_dir: List[bool] = Query(
                        default=[], description="Available only names was empty"),
                    names: List[str] = Query(
                        default=[],
                        description=("When names is empty, rename path to target, "
                                     "otherwise move these resources to target"))):
    if names:
        return {
            "message":
                f"Under <{path}> {','.join(name for name in names)} moved to <{target}>"
        }
    # use the last part of target split by '/' as new name
    new_name = target.rsplit("/", 1)[-1]
    return {"message": f"rename dir: {path} to {new_name}"}
