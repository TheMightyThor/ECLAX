'''
Created on Jul 5, 2015

@author: Theo
'''
import logging
import os

import jinja2 
from hog_functions import services, hog_cookies
import webapp2
from hog_models.model import Picture, Feature
from hog_models.UserManagement import PlayerInfo, User


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join( os.path.dirname ( __file__), os.path.pardir)),
    extensions=['jinja2.ext.autoescape'])

class AddPlayerInfo(webapp2.RequestHandler):
    
    def get(self):

        feature = Feature()
        feature.isLoggedIn = hog_cookies.get_logged_in_cookie(self)
        logging.info('Feature logged in = '+ str(feature.isLoggedIn))
        authUserId = hog_cookies.get_logged_in_cookie_user_id(self)
        authUser = User.get(authUserId)
        if authUser is not None:
            feature.isPlayer = authUser.isPlayer
        else:
            feature.isPlayer = False
            
        players = User.all().filter('isPlayer =', True).run()        
        template_values = {
            'players': players,
            'feature' : feature,
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/addPlayerInfo.html')                   
        self.response.write(template.render(template_values))
    
    def post(self):
        
        newPlayerInfo = PlayerInfo()
        playerKey = hog_cookies.get_logged_in_cookie_user_id(self)
        if playerKey is not None:
            newPlayerInfo.userKey = playerKey
        newPlayerInfo.position = self.request.get('position')
        newPlayerInfo.playerNumber = int(self.request.get('playerNumber'))
        newPlayerInfo.college = self.request.get('college')
        newPlayerInfo.highSchool = self.request.get('highSchool')
        newPlayerInfo.age = int(self.request.get('age'))
        
        newPlayerInfo.put()
        user = User.get(playerKey)
        user.playerInfo = newPlayerInfo
        user.put()
        
        redirectPage = self.request.get('current_page')
        
        self.redirect('/' + redirectPage)

app = webapp2.WSGIApplication([                                     
                                       ('/userManagement/addPlayerInfo', AddPlayerInfo),
                                       ], debug=True)
