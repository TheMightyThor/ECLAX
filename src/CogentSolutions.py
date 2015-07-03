import os
import jinja2
import webapp2
from model import mccdata_key, MCCData, User, Message, messages_key, EmailMessage, email_key

import csv
from csv import Dialect, excel
import logging
from DataQuery import DB__populateDbWithMCCCodeData, DB__deleteAllMccData, DB__selectMccCode, DB_selectAllDataOfMCCCodeType, DB_selectAllCategories
from csvImport import getCsvData

CATEGORIES = DB_selectAllCategories()

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

DEFAULT_USER_NAME = 'default_user_name'

CURRENT_USER_NAME = 'not correct'


class LogIn(webapp2.RequestHandler):
    
    
    def get(self):
                
        template = JINJA_ENVIRONMENT.get_template('html/login.html')
        self.response.write(template.render())
        self.response.set_cookie('loginCookie', '1', max_age=360, path='/', 
                        domain='None', secure=True)
class MainPage(webapp2.RequestHandler):
    
    def post(self):
      
        current_user_name = self.request.get('user_name')
        current_user_email = self.request.get('email')
        newuser = User()
        newuser.populate(username= current_user_name,
                                    email = current_user_email)
        new_userKey = newuser.put()
        userfromdb = new_userKey.get()    
        global CURRENT_USER_NAME
        CURRENT_USER_NAME = userfromdb.username
        currentNews = ['TestTile1', 'TestTitle2', 'TestTile3']    
        template_values = {
            'name': CURRENT_USER_NAME,
            'news' : currentNews,
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/index.html')
        self.response.write(template.render(template_values))
        
        
                                                    
    def get(self):
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
            'name': CURRENT_USER_NAME,
            'news' : messages,
        }
        template = JINJA_ENVIRONMENT.get_template('html/index.html')
        self.response.write(template.render(template_values))
        
class About (webapp2.RequestHandler):
    
    def get(self):
        
        template_values = {
            'name': CURRENT_USER_NAME,
                        }
         
        template = JINJA_ENVIRONMENT.get_template('html/about.html')
        self.response.write(template.render(template_values))
        
class Contact (webapp2.RequestHandler):
        
    def get(self):     
        
        template_values = {
            'name': CURRENT_USER_NAME,
        }
        template = JINJA_ENVIRONMENT.get_template('html/contact.html')
        self.response.write(template.render(template_values))
        
class Gallery (webapp2.RequestHandler):
        
    def get(self):
        
        template_values = {
            'name': CURRENT_USER_NAME,
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/gallery.html')
        self.response.write(template.render(template_values))        
        
class News (webapp2.RequestHandler):
    
    def post(self):
        new_message = Message(parent=messages_key('Messages'))
        new_message.populate(author = 'andrew',
                             email = 'andrewtheobald43@gmail.com',
                             title = 'test title',
                             message = ' short message about testing the db',
                             )
        new_message.put()
        
        message_query = Message.query(
            ancestor=messages_key('Messages')).order(-Message.date)
        messages = message_query.fetch(5) 
        
        template_values = {
            'name': CURRENT_USER_NAME,
            'messages': messages
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/news.html')                   
        self.response.write(template.render(template_values))
    
    def get(self):
        
        message_query = Message.query(
            ancestor=messages_key('Messages')).order(-Message.date)
        messages = message_query.fetch(5) 
       
        template_values = {
            'name': CURRENT_USER_NAME,
            'messages': messages
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/news.html')                   
        self.response.write(template.render(template_values))
        
class ViewEmail(webapp2.RequestHandler):
    
    def get(self):
        email_query = EmailMessage.query(
            ancestor=email_key('Email')).order(-EmailMessage.date)
        emails = email_query.fetch(5) 
        template_values = {
            'name': CURRENT_USER_NAME,
            'emails': emails
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/viewemail.html')                   
        self.response.write(template.render(template_values))
        
class Animation(webapp2.RequestHandler):
    
    def get(self):
        
        template_values = {
                           }
        template = JINJA_ENVIRONMENT.get_template('html/animation.html')
        
        self.response.write(template.render(template_values))
        
class PopulateDb(webapp2.RequestHandler):
    
    def get(self):
        
        codesFromCSV = getCsvData()
       
        for row in codesFromCSV:
           
            DB__populateDbWithMCCCodeData(row)         
                
class SelectAll(webapp2.RequestHandler):
    
    def get(self):
         
        codes = DB_selectAllDataOfMCCCodeType()
        
        template_values = {
            'codes': codes,
        }
        template = JINJA_ENVIRONMENT.get_template('html/result.html')                   
        self.response.write(template.render(template_values))
        
    
class InputData(webapp2.RequestHandler):
    
    def get(self):
        template_values = {
                           }
        
        template = JINJA_ENVIRONMENT.get_template('html/inputData.html')
        self.response.write(template.render(template_values))   
        
    def post(self):
        self.response.write("posted to one")
        
class NumberCrunch(webapp2.RequestHandler):
    
    def get(self):
       
        
        template_values = {
                           'categories' : CATEGORIES,
                           }
        
        template = JINJA_ENVIRONMENT.get_template('html/numberCrunch.html')
        self.response.write(template.render(template_values))   
        
    def post(self):
        self.response.write("posted to one")
        

        
        
application = webapp2.WSGIApplication([
                                       ('/', MainPage),
                                       ('/login', LogIn),
                                       ('/about', About),
                                       ('/news', News),
                                       ('/contact', Contact),
                                       ('/gallery', Gallery),
                                       ('/index', MainPage),
                                       ('/viewemail', ViewEmail),
                                       ('/inputData', InputData),
                                       ('/populateDb', PopulateDb),
                                       ('/selectall', SelectAll),
                                       ('/numberCrunch', NumberCrunch),
                                        ], debug=True)



