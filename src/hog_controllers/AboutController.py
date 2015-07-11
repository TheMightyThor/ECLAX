'''
Created on Jul 5, 2015

@author: Theo
'''
import logging
import os

import jinja2 
from hog_functions import services
import webapp2
from hog_models.model import User, Message, Picture, Feature, Event


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join( os.path.dirname ( __file__), os.path.pardir)),
    extensions=['jinja2.ext.autoescape'])

class About(webapp2.RequestHandler):
    
    def get(self):
        
        '''new_message = Message(parent=messages_key('Messages'))
        new_message.populate(author = 'andrew',
                             email = 'andrewtheobald43@gmail.com',
                             title = 'test title',
                             message = ' short message about testing the db',
                             )
        new_message.put()'''
        
        feature = Feature()

        feature.isLoggedIn = True
        messages = Message.all().order('date').run(limit=8)
        
        
        template_values = {
            'news': messages,
            'feature' : feature,
        }
        
        template = JINJA_ENVIRONMENT.get_template('/html/underdevelopment.html')                   
        self.response.write(template.render(template_values))
    


app = webapp2.WSGIApplication([                                     
                                       ('/about/', About),
                                       ], debug=True)
