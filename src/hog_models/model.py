'''
Created on Sep 20, 2013

@author: Theo
'''
from google.appengine.ext import db


class Picture(db.Model):
    title = db.StringProperty()
    picture = db.BlobProperty(default=None)
    id = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class User(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    email = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    isPlayer = db.BooleanProperty()
    isAdmin = db.BooleanProperty()
    cell_number = db.IntegerProperty()
    cell_carrier = db.IntegerProperty()
 
class Event(db.Model):
    day = db.IntegerProperty()
    month = db.IntegerProperty()
    yaer = db.IntegerProperty()
    title = db.StringProperty()


class Feature(db.Model):
    isPlayer = db.BooleanProperty()
    isLoggedIn = db.BooleanProperty()
    
class Message(db.Model):
    
    author = db.StringProperty()
    email = db.StringProperty()
    title = db.StringProperty()
    message = db.StringProperty()
    internalOnly = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
