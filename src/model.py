'''
Created on Sep 20, 2013

@author: Theo
'''
from google.appengine.ext import ndb

DEFAULT_USER_NAME = "Users"

DEFAULT_MESSAGE = "Messages"

DEFAULT_MCCDATA = "MccData"

def user_key(user_name=DEFAULT_USER_NAME):

    return ndb.Key('Users', user_name)

def mccdata_key(mccdata_key=DEFAULT_MCCDATA):
    
    return ndb.Key('MccData', mccdata_key)

class Movie(ndb.Model):
    title = ndb.StringProperty()
    picture = ndb.BlobProperty(default=None)
    id = ndb.StringProperty()

class User(ndb.Model):
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
 
def messages_key(messages_key=DEFAULT_MESSAGE):
    
    return ndb.Key('Messages', messages_key)
    
class Message(ndb.Model):
    
    author = ndb.StringProperty()
    email = ndb.StringProperty()
    title = ndb.StringProperty()
    message = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
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