'''
Created on Jul 16, 2015

@author: Theo
'''
from google.appengine.ext import db
from google.appengine.ext import ndb


class PlayerInfo(db.Model):
    position = db.StringProperty(default="Bench")
    picture = db.BlobProperty(default=None)
    userKey = db.StringProperty()
    playerNumber = db.IntegerProperty(default = 69)
    college = db.StringProperty()
    highSchool = db.StringProperty()
    age = db.IntegerProperty()

class User(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    email = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    isPlayer = db.BooleanProperty()
    isAdmin = db.BooleanProperty()
    cell_number = db.IntegerProperty()
    cell_carrier = db.IntegerProperty()
    
    @property
    def keyasstring(self):
        return str(self.key())

def get_user_player_info(key):
    return PlayerInfo.get(key)