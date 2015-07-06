import os
import jinja2
import webapp2
from webapp2_extras import sessions, securecookie
from model import mccdata_key, MCCData, User, Message, messages_key, EmailMessage, email_key, Movie
import cgi
import csv
import urllib
from csv import Dialect, excel
import logging
from DataQuery import DB__populateDbWithMCCCodeData, DB__deleteAllMccData, DB__selectMccCode, DB_selectAllDataOfMCCCodeType, DB_selectAllCategories
from csvImport import getCsvData

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

CATEGORIES = DB_selectAllCategories()
'''PATH_TO_IMAGES = os.path.dirname(os.path.abspath(__file__)) + '/gallery'''

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

DEFAULT_USER_NAME = 'default_user_name'

CURRENT_USER_NAME = 'not correct'

class BaseController (webapp2.RequestHandler):
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
        # Returns a session using the default cookie key.
        
class NewUser(webapp2.RequestHandler):
    
    def get(self):
      
        
        template = JINJA_ENVIRONMENT.get_template('html/newuser.html')
        self.response.write(template.render())
        
    def post(self):
        newUser = User()
        newUser.username = self.request.get('user_name')
        newUser.email = self.request.get('email')
        newUser.password = self.request.get('password')
        
        exist = User.all().filter('email', newUser.email).get()
        
        if exist:
            self.response.write('Email already exists')
            
        else:
            newUser.put()
            self.response.write('Alright')
        
class LogIn(BaseController):
           
    
    def post(self):
        redirect = self.request.get('current_page')
        user = User()
        user.username =self.request.get('user_name')
        user.password = self.request.get('password')
        authUser = User.all().filter('username =', user.username).get()
        
        logging.info('Pw' + user.password + " authPW " + authUser.password)
        if authUser:
            if user.password == authUser.password:
                self.response.set_cookie('loginCookie', '1', max_age=360, path='/', 
                        domain='None', secure=True)
                
                
                self.redirect('/'+ redirect)
                
            else:
                self.response.write('Incorrect password or username')
            
class MainPage(webapp2.RequestHandler):
    
    def post(self):
      
        self.request.get_cookie
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
        now = datetime.datetime.now()
        events = Event.all().filter('month =', now.month).filter('year =', now.year).run()
   
        messages = Message.all().order('date').run(limit=8)
        
        
        images = Movie.all().run(limit=10)
        imageTitles = []
        for image in images:
            logging.info("id = " + image.title)
            imageTitles.append(image.title)

            
        logging.info(imageTitles.__str__())
        template_values = {
            'name': CURRENT_USER_NAME,
            'news' : messages,
            'imageTitles' : imageTitles,
            'events' : events,
        }
        template = JINJA_ENVIRONMENT.get_template('html/index.html')
       
        self.response.write(template.render(template_values))
        #self.response.headers['Content-Type'] = 'image/png'
        
class Image(webapp2.RequestHandler):
    def get(self):
        #image_query = Movie.query(ancestor=messages_key('Images')) 
        #images = image_query.fetch(1)
        #logging.info(images[0].title + '*****')
        
        #logging.info(" ID FROM REQUEST = " + urlsafe=self.request.get("pic_title"))
        pic =  self.request.get("pic_title")
      
        p = Movie.all().filter('title =', pic).get()
        #.run(limit=1):
        #for p in images:
            
        if p:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(p.picture)
        else:
            self.response.out.write('No image')

        
class PostImage(webapp2.RequestHandler):        
            
        def post(self):
            image = Movie()
            image.title = self.request.get('image_name')       
            image.picture = self.request.get('img')
            image.put()
            redirect = self.request.get("current_page")
            self.redirect('/'+ redirect)
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
                                       ('/contact', Contact),
                                       ('/gallery', Gallery),
                                       ('/index', MainPage),
                                       ('/newuser', NewUser),
                                       ('/img', Image),
                                       ('/postImage', PostImage),
                                       ('/viewemail', ViewEmail),
                                       ('/inputData', InputData),
                                       ('/populateDb', PopulateDb),
                                       ('/selectall', SelectAll),
                                       ('/numberCrunch', NumberCrunch),
                                        ], debug=True, config=config)



