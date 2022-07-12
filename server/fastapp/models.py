
import databases
import sqlalchemy

import ormar

from .config import DATABASE_URL
# get your database url in sqlalchemy format - same as used with databases instance used in Model definition
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={'check_same_thread': False})
# metadata.create_all(engine)

class User(ormar.Model):
    class Meta:
        database = database
        metadata = metadata

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    completed: bool = ormar.Boolean(default=False)
