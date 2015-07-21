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
from hog_models.UserManagement import PlayerInfo, User, get_user_player_info


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join( os.path.dirname ( __file__), os.path.pardir)),
    extensions=['jinja2.ext.autoescape'])

class About(webapp2.RequestHandler):
    
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
        for player in players:
            key = str(player.key)
            #playerInfo = get_user_player_info(key)
            #if playerInfo is not None:
            #    player.playerInfo = playerInfo
        template_values = {
            'players': players,
            'feature' : feature,
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/about.html')                   
        self.response.write(template.render(template_values))
    


app = webapp2.WSGIApplication([                                     
                                       ('/about/', About),
                                       ], debug=True)
