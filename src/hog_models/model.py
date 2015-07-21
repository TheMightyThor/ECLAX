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


class Feature(db.Model):
    isPlayer = db.BooleanProperty()
    isLoggedIn = db.BooleanProperty()
    
class Message(db.Model):
    
    author = db.StringProperty()
    email = db.StringProperty()
    title = db.StringProperty()
    message = db.TextProperty()
    internalOnly = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
