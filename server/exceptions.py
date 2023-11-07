from typing import Any, List

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


class BaseException(Exception):
    detail: str
    status_code: int = HTTP_400_BAD_REQUEST


class ArgsLengthNotEqual(BaseException):
    def __init__(self, names: List[str], field: List[Any]) -> None:
        length = ", ".join(f"{name}({len(value)})" for name, value in zip(names, field))
        self.detail = f"Length of {length} not equal"


class FieldCheckError(BaseException):
    """Raised when a field is not valid"""

    def __init__(self, field_name: str, field: Any) -> None:
        self.detail = f"{field_name}<{field}> is not valid"


class InvalidRequest(BaseException):
    """Raised when root path is renamed"""

    def __init__(self, detail: str = "") -> None:
        self.detail = detail
        super().__init__()


class InvalidLogin(BaseException):
    """Raised when authentication failed"""

    status_code: int = HTTP_401_UNAUTHORIZED
    detail: str = "Authentication failed"


class ResourceNotFound(BaseException):
    """Raised when a resource is not found"""

    def __init__(self, resource) -> None:
        self.detail = f"Resource<{resource}> not found."
        super().__init__()


class ResourceAlreadyExists(BaseException):
    """Raised when a resource already exists"""

    def __init__(self, resource) -> None:
        self.detail = f"Resource<{resource}> already exists."
        super().__init__()
