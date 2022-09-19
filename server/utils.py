import os
from hashlib import md5


def create_token(password: str, expired_time: int) -> str:
    app_key = os.getenv("APPKEY")
    if not app_key:
        raise ValueError("APPKEY not found")
    encryptor = md5()
    encryptor.update(password.encode())
    encryptor.update(app_key.encode())
    encryptor.update(expired_time.to_bytes(8, "big"))
    return encryptor.hexdigest()
