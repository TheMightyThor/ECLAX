'''
Created on Jul 18, 2015

@author: Theo
'''
from google.appengine.ext import db
from google.appengine.ext.db import DateTimeProperty, StringProperty,\
    ListProperty, BooleanProperty

class GameEvent(db.Model):
    date = StringProperty()
    location = StringProperty()
    name = StringProperty()
    roster = ListProperty(StringProperty().datastore_type(),default=None)
    outRoster = ListProperty(StringProperty().datastore_type(),default=None)
    details = StringProperty()
    isInternal = BooleanProperty()
    urlKey = StringProperty()