from email.policy import default
from hashlib import md5

import ormar

from .base import BaseConfig, BaseMeta


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user"

    class Config(BaseConfig):
        ...

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    username: str = ormar.String(max_length=80, unique=True)  # type: ignore
    password: str = ormar.String(max_length=32)  # type: ignore
    is_admin: bool = ormar.Boolean(default=False)

    def validate_password(self, password: str) -> bool:
        return md5(password.encode("utf-8")).hexdigest() == self.password

    async def set_password(self, password: str) -> "User":
        new_password = md5(password.encode("utf-8")).hexdigest()
        return await self.update(password=new_password)

    async def set_username(self, username: str) -> "User":
        return await self.update(username=username)
