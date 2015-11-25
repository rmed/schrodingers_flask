from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

# Database information from app configuration (when started)
db_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = db_proxy


class User(BaseModel):
    """ Users of the platform. """

    username = CharField(max_length=64, unique=True)
    password = CharField()
    email = CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'users'

    def check_password(self, password):
        """ Check password against the stored hash. """
        return check_password_hash(self.password, password)

    @classmethod
    def generate_password(cls, password):
        """ Generate a password hash. """
        return generate_password_hash(password)


class Nya(BaseModel):
    """ Public messages in our platform. """

    author = ForeignKeyField(User, related_name='nyas')
    message = CharField(max_length=160)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    class Meta:
        db_table = 'nyas'


class Subscription(BaseModel):
    """ Users can follow other users. """
    subscriber = ForeignKeyField(User, related_name='subscriptions')
    publisher = ForeignKeyField(User, related_name='subscribers')

    class Meta:
        db_table = 'subscriptions'
        indexes = (
            (('subscriber', 'publisher'), True),
        )
