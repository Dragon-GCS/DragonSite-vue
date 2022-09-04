from typing import Any, List

from ormar import Model


class BaseException(Exception):
    msg: str

    def __str__(self) -> str:
        return self.msg


class ArgsLengthNotEqual(BaseException):
    def __init__(self, names: List[str], field: List[Any]) -> None:
        length = ", ".join(f"{name}({len(value)})" for name, value in zip(names, field))
        self.msg = f"Length of {length} not equal"


class FieldCheckError(BaseException):
    """Raised when a field is not valid"""
    def __init__(self, field_name: str, field: Any) -> None:
        self.message = f"{field_name}<{field}> is not valid"


class ResourceNotFound(BaseException):
    """Raised when a resource is not found"""
    def __init__(self, resource) -> None:
        self.msg = f"Resource<{resource}> not found."


class RootRenameError(BaseException):
    """Raised when root path is renamed"""
    def __init__(self) -> None:
        self.msg = "Root path can not be renamed."