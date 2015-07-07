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

class News(webapp2.RequestHandler):
    
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
        
        template = JINJA_ENVIRONMENT.get_template('html/news.html')                   
        self.response.write(template.render(template_values))
    
class MessageDetail(webapp2.RequestHandler):    
    def get(self):
        id = self.request.get("message_id")
        message = Message()
        self.response.write(id)

class NewMessage(webapp2.RequestHandler):
    
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('html/newmessage.html')   
        self.response.write(template.render())
    
    def post (self):
        currentPage = self.request.get('current_page')
        newMessage = Message()
        if self.request.get("internal"):
            newMessage.internalOnly = True 
        newMessage.author = self.request.get("user_name")
        newMessage.message = self.request.get("message_area")
        newMessage.title = self.request.get("title")
       
        newMessage.put()      
        emailAll = self.request.get("emailAll")
       
        if emailAll:
            users = User.all().filter("isPlayer =", True)
            if users:
                for user in users:
                    services.email_user(user.email, user.username, newMessage.message, newMessage.title)
                
                
        self.redirect(currentPage)
app = webapp2.WSGIApplication([                                     
                                       ('/news/messagedetail', MessageDetail),
                                       ('/news/newmessage', NewMessage),
                                       ('/news/', News),
                                       ], debug=True)
