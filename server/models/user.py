import base64
import hashlib

import ormar

from server.config import APP_KEY

from .base import BaseConfig, BaseMeta


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user"

    class Config(BaseConfig):
        ...

    id: int = ormar.Integer(primary_key=True)  # type: ignore
    username: str = ormar.String(max_length=80, unique=True)  # type: ignore
    password: str = ormar.String(  # type: ignore
        max_length=128, encrypt_secret=APP_KEY, encrypt_backend=ormar.EncryptBackends.HASH
    )
    is_admin: bool = ormar.Boolean(default=False)

    def encrypt_password(self, password: str) -> str:
        secret = hashlib.sha256(APP_KEY.encode()).digest()
        secret = base64.urlsafe_b64encode(secret)
        return hashlib.sha512(secret + password.encode()).hexdigest()

    def validate_password(self, password: str) -> bool:
        return self.encrypt_password(password) == self.password

    def generate_token(self, expired_time: int, password: str = "") -> str:
        encryptor = hashlib.md5()
        encryptor.update(APP_KEY.encode())
        encryptor.update((password or self.password).encode())
        encryptor.update(expired_time.to_bytes(8, "big"))
        return encryptor.hexdigest()

    def validate_token(self, token: str, expired_time: int) -> bool:
        return self.generate_token(expired_time) == token
