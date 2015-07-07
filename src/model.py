'''
Created on Sep 20, 2013

@author: Theo
'''
from google.appengine.ext import ndb
from google.appengine.ext import db
DEFAULT_USER_NAME = "Users"

DEFAULT_MESSAGE = "Messages"

DEFAULT_MCCDATA = "MccData"

def user_key(user_name=DEFAULT_USER_NAME):

    return ndb.Key('Users', user_name)

def mccdata_key(mccdata_key=DEFAULT_MCCDATA):
    
    return ndb.Key('MccData', mccdata_key)

class Picture(db.Model):
    title = db.StringProperty()
    picture = db.BlobProperty(default=None)
    id = db.StringProperty()

class User(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    email = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    isPlayer = db.BooleanProperty()
    isAdmin = db.BooleanProperty()
 
def messages_key(messages_key=DEFAULT_MESSAGE):
    
    return ndb.Key('Messages', messages_key)
 
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
    
def email_key(email_key=DEFAULT_MESSAGE):
    
    return ndb.Key('Email', email_key)
    
class EmailMessage(ndb.Model):
    
    sender = ndb.StringProperty()
    subject = ndb.StringProperty()
    owner = ndb.StringProperty(indexed=True)
    message_body = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class MCCData(ndb.Model):
    
    mccCode = ndb.StringProperty(indexed=True)
    category = ndb.StringProperty()
    percentVol = ndb.FloatProperty()
    percentCount = ndb.FloatProperty()
    rate = ndb.FloatProperty()
    transactionFee = ndb.FloatProperty()
    
    @classmethod
    def query_mcc_data(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)