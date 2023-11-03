from typing import Any, List

from fastapi import HTTPException, status


class BaseException(HTTPException):
    detail: str
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class ArgsLengthNotEqual(BaseException):
    def __init__(self, names: List[str], field: List[Any]) -> None:
        length = ", ".join(f"{name}({len(value)})" for name, value in zip(names, field))
        self.detail = f"Length of {length} not equal"
        super().__init__()


class FieldCheckError(BaseException):
    """Raised when a field is not valid"""

    def __init__(self, field_name: str, field: Any) -> None:
        self.detail = f"{field_name}<{field}> is not valid"
        super().__init__()


class ResourceNotFound(BaseException):
    """Raised when a resource is not found"""

    def __init__(self, resource) -> None:
        self.detail = f"Resource<{resource}> not found."
        super().__init__()


class RootRenameError(BaseException):
    """Raised when root path is renamed"""

    def __init__(self) -> None:
        self.detail = "Root path can not be renamed."
        super().__init__()


class AuthError(BaseException):
    """Raised when authentication failed"""

    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, detail: str = "Authentication failed") -> None:
        self.detail = detail
        super().__init__()
