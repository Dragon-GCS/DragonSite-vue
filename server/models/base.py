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
