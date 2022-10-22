import os
from enum import Enum
from pathlib import Path

# Set DEBUG environment variable to True to enable debug mode
DEBUG = bool(os.environ.get("DEBUG"))

DBNAME = "test.sqlite" if DEBUG else os.environ.get("DBNAME", "db.sqlite")

# root directory is server folder
ROOT = Path(__file__).parent.absolute()

# database dir
DATABASE_DIR = ROOT / DBNAME
DATABASE_URL = f"sqlite:///{DATABASE_DIR}"
# static files dir
FILE_DIR = ROOT / "../files"
FILE_DIR.mkdir(parents=True, exist_ok=True)
# frontend dist dir
DIST_DIR = ROOT / "../dist"

# regex for validating file name
FILENAME_REGEX = r"[^/\\:<>\*\|\?\.\"]"
# regex for validating file path
FILE_PATH_REGEX = rf"^(/{FILENAME_REGEX}+)+|/$"

# cookie validity
COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days


class FileCats(Enum):
    """ file categories enum"""
    ALL = "all"
    AUDIO = "audio"
    DOCUMENT = "document"
    IMAGE = "image"
    OTHER = "other"
    TEXT = "text"
    VIDEO = "video"
    NONE = ""

    @classmethod
    def sort_mime_type(cls, mime_type: str) -> str:
        """Sort different mime types to file categories.
        Args:
            mime_type: file's mime_type
        Returns:
            the file category
        """
        if not mime_type:
            return cls.NONE.value
        if mime_type.startswith("audio"):
            return cls.AUDIO.value
        if mime_type.startswith("video"):
            return cls.VIDEO.value
        if mime_type.startswith("image"):
            return cls.IMAGE.value
        if mime_type.startswith("text"):
            return cls.TEXT.value
        if "document" in mime_type or mime_type.endswith("pdf"):
            return cls.DOCUMENT.value
        return cls.OTHER.value
