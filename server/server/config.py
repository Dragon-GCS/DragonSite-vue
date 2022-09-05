import os
from enum import Enum
from pathlib import Path

# Set DEBUG environment variable to True to enable debug mode
DEBUG = bool(os.environ.get("DEBUG"))

DBNAME = "test.sqlite" if DEBUG else os.environ.get("DBNAME", "db.sqlite")

# root directory is server folder
ROOT = Path(__file__).parent.parent.absolute()
PORT = 8888

# database dir
DATABASE_DIR = ROOT / DBNAME
DATABASE_URL = f"sqlite:///{DATABASE_DIR}"
# static files dir
FILE_DIR = ROOT / "files"
# frontend dist dir
DIST_DIR = ROOT / "../dist"

# regex for validating file name
FILENAME_REGEX = r"[^/:<>\\\*\|]"
# regex for validating file path
FILE_PATH_REGEX = rf"^(/{FILENAME_REGEX}+)+|/$"


class FileCats(Enum):
    """ file categories enum"""
    ALL = "all"
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    DOCUMENT = "document"
    OTHER = "other"
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
        if "audio" in mime_type:
            return cls.AUDIO.value
        if "video" in mime_type:
            return cls.VIDEO.value
        if "image" in mime_type:
            return cls.IMAGE.value
        if "document" in mime_type:
            return cls.DOCUMENT.value
        return cls.OTHER.value