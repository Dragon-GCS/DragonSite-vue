import os
from enum import Enum
from pathlib import Path

# Set DEBUG environment variable to True to enable debug mode
DEBUG = bool(os.environ.get("DEBUG"))

# root directory is server folder
ROOT = Path(__file__).parent.absolute()

# app key, default is not safe change to your own app key
DEFAULT_APP_KEY = "1234567890"
APP_KEY = os.getenv("APP_KEY", DEFAULT_APP_KEY)

# database url, change to your own database url
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'db.sqlite'}")
# DATABASE_URL = "protocol://<username>:<password>@<host>:<port>/<database>"

# test database url
if DEBUG:
    DATABASE_URL = f"sqlite:///{ROOT / 'test.sqlite'}"

# static files dir
FILE_DIR = ROOT / "../files"
FILE_DIR.mkdir(parents=True, exist_ok=True)

# preview resolution
THUMBNAIL_SIZE = (64, 64)

# frontend dist dir
DIST_DIR = ROOT / "../dist"

# cookie validity
COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days


class FileTypeEnum(Enum):
    """file categories enum"""

    AUDIO = "audio"
    DOCUMENT = "document"
    IMAGE = "image"
    OTHER = "other"
    TEXT = "text"
    VIDEO = "video"
    NONE = ""

    @classmethod
    def sort_by_mime(cls, mime_type: str | None) -> "FileTypeEnum":
        """Sort different mime types to file categories.
        Args:
            mime_type: file's mime_type
        Returns:
            the file category
        """
        if not mime_type:
            return cls.NONE
        if mime_type.startswith("audio"):
            return cls.AUDIO
        if mime_type.startswith("video"):
            return cls.VIDEO
        if mime_type.startswith("image"):
            return cls.IMAGE
        if mime_type.startswith("text"):
            return cls.TEXT
        if "document" in mime_type or mime_type.endswith("pdf"):
            return cls.DOCUMENT
        return cls.OTHER
