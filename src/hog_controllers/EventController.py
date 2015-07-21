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
from hog_models.GameEvent import GameEvent
from hog_models.UserManagement import PlayerInfo, User, get_user_player_info


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join( os.path.dirname ( __file__), os.path.pardir)),
    extensions=['jinja2.ext.autoescape'])

class Events(webapp2.RequestHandler):
    
    def get(self):

        feature = Feature()
        feature.isLoggedIn = hog_cookies.get_logged_in_cookie(self)
        
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
        title = self.request.get('eventName')
        gameEvent = GameEvent.all().filter('name =', title).run()
        path = self.request.path()
        logging.info(path)
        User.get(gameEvent.roster)
        template_values = {
            'players': players,
            'feature' : feature,
            'event' : gameEvent,
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/event.html')                   
        self.response.write(template.render(template_values))
    

class CreateEvent(webapp2.RequestHandler):
   
    def get(self):
        template_values = {
                          }
        template = JINJA_ENVIRONMENT.get_template('html/createEvent.html')                   
        self.response.write(template.render(template_values))
   
    def post(self):
        newEvent = GameEvent()
        title = self.request.get('title')
        if title is not None:
            newEvent.name = title 
        details = self.request.get('details')
        if details is not None:
            newEvent.details = details
        date = self.request.get('date')
        if date is not None:
            newEvent.date = date
        internal = self.request.get('internal')
        if internal is 1:
            newEvent.isInternal = True
        else:
            newEvent.isInternal = False
        emailAll = self.request.get('emailAll')
        if emailAll is not None:
            message = newEvent.details
            services.roster_email_all_user(message, title)
        sendText = self.request.get('send_text')
        if sendText is not None:
            logging.info("sendText")
            
        newEvent.put()
        self.redirect('/index')
        
class EventInfo(webapp2.RequestHandler):
    
    def get(self):
        
        eventKey = self.request.get('eventname')
        gameEvent = GameEvent.all().filter('name =', eventKey).get()    
        roster = User.get(gameEvent.roster)
        outRoster = User.get(gameEvent.outRoster)
        logging.info(roster)
        template_values = {
                           'event' : gameEvent,
                           'roster' : roster,
                           'outRoster': outRoster,
                           }
        template = JINJA_ENVIRONMENT.get_template('html/eventDetails.html')                   
        self.response.write(template.render(template_values))
        
    def post(self):
        
        playa = hog_cookies.get_logged_in_cookie_user_id(self)
        isPlaying = self.request.get('isPlaying')
        logging.info(' IS PLAYING = ' +isPlaying)
        eventName = self.request.get('eventName')
        logging.info('Event Name = ' +eventName)
        if isPlaying:
            gameEvent = GameEvent.all().filter('name =', eventName).get()
            gameEvent.roster.append(playa)
            gameEvent.put()
            roster = User.get(gameEvent.roster)
            logging.info(roster)
            template_values = {
                               'event' : gameEvent,
                               'roster' : roster,
                               }
            template = JINJA_ENVIRONMENT.get_template('html/eventDetails.html')                   
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')
    
app = webapp2.WSGIApplication([                                     
                                       ('/events/', Events),
                                       ('/events/createEvent', CreateEvent),
                                       ('/events/event', EventInfo)
                                       ], debug=True)
