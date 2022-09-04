from datetime import datetime
from typing import Any, List

import databases
import ormar
import sqlalchemy

from server.config import DATABASE_URL

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class BaseConfig:
    anystr_strip_whitespace = True
    fields = {
        "parent": {
            "exclude": True
        },
        "name": {
            "exclude": True
        },
        "parent_path": {
            "exclude": True
        },
    }


class AutoUpdateModified(ormar.QuerySet):
    async def update(self, each: bool = False, **kwargs: Any) -> int:
        if "modified_time" in self.__dict__:
            self.modified_time = datetime.now()
        return await super().update(each, **kwargs)

    async def bulk_update(self,
                          objects: List[ormar.Model],
                          columns: List[str] = []) -> None:
        for object in objects:
            if "modified_time" in object.__dict__:
                object.modified_time = datetime.now()
        return await super().bulk_update(objects, columns)
