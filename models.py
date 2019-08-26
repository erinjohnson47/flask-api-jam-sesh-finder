from peewee import *
from flask_login import UserMixin
import datetime 


DATABASE = SqliteDatabase('jamss.sqlite') 

class BaseModel(Model):
    class Meta:
        database = DATABASE

class User(UserMixin, BaseModel):
    username = CharField(unique = True, null = False) 
    email = CharField(unique = True, null = False) 
    password = CharField(null = False)
    image = CharField()
    location = CharField()


# when we initalize this it will be of type class Model
class Event(BaseModel):
    title = CharField()
    date = DateField('%Y-%m-%d')
    start_time = TimeField('%H:%M')
    end_time = TimeField('%H:%M')
    location = CharField()
    created_by = ForeignKeyField(User, backref='events')
    created_at = DateTimeField(default=datetime.datetime.now)


class UserEvent(BaseModel):
    user = ForeignKeyField(User, backref='users')
    event = ForeignKeyField(Event, backref='events')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Event, UserEvent], safe=True) 
    print("TABLES CREATED")
    DATABASE.close()



