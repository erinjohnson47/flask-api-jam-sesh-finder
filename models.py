from peewee import *
from flask_login import UserMixin
import datetime 


DATABASE = SqliteDatabase('jam.sqlite') 



class User(UserMixin, Model):
    username = CharField(unique = True, null = False) 
    email = CharField(unique = True, null = False) 
    password = CharField(null = False)
    image = CharField()
    location = CharField()

    class Meta:
        database = DATABASE

# when we initalize this it will be of type class Model
class Event(Model):
    title = CharField()
    date = DateField('%Y-%m-%d')
    start_time = TimeField('%H:%M')
    end_time = TimeField('%H:%M')
    location = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE # database property coming from Model




def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Event], safe=True) 
    print("TABLES CREATED")
    DATABASE.close()



