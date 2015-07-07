'''
Created on Jul 5, 2015

@author: Theo
'''
import os
import jinja2
import webapp2
from model import Message, messages_key, Feature, User
import logging
import services

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
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
        
        template = JINJA_ENVIRONMENT.get_template('html/underdevelopment.html')                   
        self.response.write(template.render(template_values))
    


app = webapp2.WSGIApplication([                                     
                                       ('/about/', About),
                                       ], debug=True)
