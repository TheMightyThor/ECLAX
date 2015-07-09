import Cookie
import cgi
from csv import Dialect, excel
import csv
import datetime
import logging
import os
import urllib
import uuid

import jinja2
from model import User, Message, EmailMessage, email_key, Picture, Feature, Event
import webapp2
import security
from warnings import catch_warnings
import functions



config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

'''class BaseController (webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        backend = "securecookie" # default
        return self.session_store.get_session(backend=backend)
        # Returns a session using the default cookie key.'''
        
class NewUser(webapp2.RequestHandler):
    
    def get(self):
        
        
        template = JINJA_ENVIRONMENT.get_template('html/newuser.html')
        self.response.write(template.render())
        
    def post(self):
        newUser = User()
        newUser.email = self.request.get('email')
        exist = User.all().filter('email', newUser.email).get()
        if exist:
            self.response.write('Email already exists')
        else:
            newUser.username = self.request.get('user_name')
            pw = self.request.get('password')
            newUser.password = security.generate_password_hash(pw, method='sha1', length=22, pepper='3cH06')
            player_password = self.request.get('player_password')
            
            if '3cH06' == player_password:
                newUser.isPlayer = True                
            else:
                newUser.isPlayer = False
            
            key = newUser.put()
            
            sid = str(key)
            
            cookie_name = '='.join(('EcHogs',sid))
            self.response.headers.add_header('Set-Cookie',cookie_name)
            self.redirect('/'+ self.request.get('current_page'))
        
class LogIn(webapp2.RequestHandler):
           
    
    def post(self):
        redirect = self.request.get('current_page')
        user = User()
        user.username =self.request.get('user_name')
        password = self.request.get('password')
        logging.info('User Name = ' +user.username)
        authUser = User.all().filter('username =', user.username).get()
        if authUser is not None:
            logging.info('Authuser pw ' + authUser.password)
            logging.info('NEW PASSWORD' + security.generate_password_hash(password, method='sha1', length=22, pepper='3cH06'))
            pwHash = security.check_password_hash(password, authUser.password, '3cH06')
            if pwHash:
                logging.info("HashesMatch")                  
                self.redirect('/'+ redirect)
                    
        else:
            self.response.write('Incorrect password or username')
            
class MainPage(webapp2.RequestHandler):
    
    def post(self):            
        current_user_name = self.request.get('user_name')
        current_user_email = self.request.get('email')
        newuser = User()
        newuser.populate(username= current_user_name,
                                    email = current_user_email)
        new_userKey = newuser.put()
        
           
        template_values = {
          
            
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/index.html')
        self.response.write(template.render(template_values))
        
        
                                                    
    def get(self):
        feature = Feature()
        if self.request.cookies is not None:
            if self.request.cookies['EcHogs'] is not None:
                sid =  self.request.cookies['EcHogs']
                if sid:                
                    feature.isLoggedIn = True
                    logging.info(sid + ' IS logged in')
            
    
            try:
                other = self.request.cookies['othercookie']
            except:
                logging.info("NO other cookie")            
                          
        else:
            feature.isLoggedIn = False
       
        now = datetime.date.today()
        events = Event.all().filter('month =', now.month).filter('year =', now.year).run()
   
        messages = Message.all().order('date').run(limit=8)
        
        keys = Picture.all(keys_only=True).order('-date').run(limit=10)
        imageKeys = []
        for key in keys:
            imageKeys.append(str(key))   
    
        template_values = {
            'news' : messages,
            'imageKeys' : imageKeys,
            'events' : events,
            'feature' : feature,
        }
        template = JINJA_ENVIRONMENT.get_template('html/index.html')
         
        self.response.write(template.render(template_values))
        
        
class Image(webapp2.RequestHandler):
    def get(self):

        key =  self.request.get("pic_key")
        
        p = Picture.get(key) 
            
        if p:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(p.picture)
        else:
            self.response.out.write('No image')

        
class PostImage(webapp2.RequestHandler):        
            
        def post(self):
            image = Picture()
            image.title = self.request.get('image_name')       
            image.picture = self.request.get('img')
            image.put()
            redirect = self.request.get("current_page")
            self.redirect('/'+ redirect)

class Gallery (webapp2.RequestHandler):
        
    def get(self):
        
        template_values = {
           
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/gallery.html')
        self.response.write(template.render(template_values))        
        
    
'''class ViewEmail(webapp2.RequestHandler):
    
    def get(self):
        email_query = EmailMessage.query(
            ancestor=email_key('Email')).order(-EmailMessage.date)
        emails = email_query.fetch(5) 
        template_values = {
            'name': CURRENT_USER_NAME,
            'emails': emails
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/viewemail.html')                   
        self.response.write(template.render(template_values))'''
        
        
'''class PopulateDb(webapp2.RequestHandler):
    
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
        self.response.write("posted to one")'''      
        
application = webapp2.WSGIApplication([
                                       ('/', MainPage),
                                       ('/login', LogIn),
                                       ('/gallery', Gallery),
                                       ('/index', MainPage),
                                       ('/newuser', NewUser),
                                       ('/index/postimage', PostImage),
                                       ('/img', Image),                            
                                        ], debug=True, config=config)



