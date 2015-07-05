'''
Created on Jul 5, 2015

@author: Theo
'''
import os
import jinja2
import webapp2
from model import Message, messages_key
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class News(webapp2.RequestHandler):
    
    def get(self):
        logging.info('hit the controller')
        '''new_message = Message(parent=messages_key('Messages'))
        new_message.populate(author = 'andrew',
                             email = 'andrewtheobald43@gmail.com',
                             title = 'test title',
                             message = ' short message about testing the db',
                             )
        new_message.put()'''
      
        message_query = Message.query(
            ancestor=messages_key('Messages')).order(-Message.date)
        messages = message_query.fetch(5) 
        
        template_values = {
            'news': messages
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/news.html')                   
        self.response.write(template.render(template_values))
    
class MessageDetail(webapp2.RequestHandler):    
    def get(self):
        id = self.request.get("message_id")
        message = Message()
        self.response.write(id)

app = webapp2.WSGIApplication([
                                       ('/news/', News),
                                       ('/news/messagedetail', MessageDetail)
                                       ], debug=True)
