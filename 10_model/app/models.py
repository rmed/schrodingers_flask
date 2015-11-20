from peewee import *

# Database information from app configuration (when started)
db_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = db_proxy


class User(BaseModel):
    """ Users of the platform. """

    name = CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'users'
