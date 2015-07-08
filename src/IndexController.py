import os
import jinja2
import webapp2
from webapp2_extras import sessions, securecookie
from model import User, Message, EmailMessage, email_key, Picture, Feature, Event
import cgi
import datetime
import csv
import urllib
from csv import Dialect, excel
import logging
import Cookie
import uuid
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

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
        newUser.email = self.request.get('email')
        exist = User.all().filter('email', newUser.email).get()
        if exist:
            self.response.write('Email already exists')
        else:
            newUser.username = self.request.get('user_name')
            
            newUser.password = self.request.get('password')
            player_password = self.request.get('player_password')
            if '3cH06' == player_password:
                newUser.isPlayer = True
            else:
                newUser.isPlayer = False
            
            key = newUser.put()
            
            sid = str(key)
            ck = Cookie.SimpleCookie()
            
            ck['EcHogs2'] = str(uuid.uuid4())
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=1) # expires in 30 days
            ck['EcHogs2']['expires'] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            ck['EcHogs2']['path'] = '/'
            cookie_name = '='.join(('EcHogs',sid))
            expire_time = '='.join(('expires', expires.strftime("%a, %d %b %Y %H:%M:%S GMT")))
            ssid = ';'.join((cookie_name, expire_time))
            self.response.headers.add_header('Set-Cookie', ssid)
            logging.info(ck.output())
            self.response.headers.add_header('Set-Cookie',ck.items().__str__())
            self.redirect('/'+ self.request.get('current_page'))
        
class LogIn(BaseController):
           
    
    def post(self):
        redirect = self.request.get('current_page')
        user = User()
        user.username =self.request.get('user_name')
        user.password = self.request.get('password')
        authUser = User.all().filter('username =', user.username).get()
        
        if authUser:
            if user.password == authUser.password:
                self.response.set_cookie('loginCookie', '1', max_age=360, path='/', 
                        domain='None', secure=True)
                
                
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
            'name': CURRENT_USER_NAME,
            
        }
        
        template = JINJA_ENVIRONMENT.get_template('html/index.html')
        self.response.write(template.render(template_values))
        
        
                                                    
    def get(self):
        feature = Feature()
        if self.request.cookies:
            if self.request.cookies['EcHogs']:
                sid =  self.request.cookies['EcHogs']
                if sid:
                    decode = Cookie.BaseCookie.value_decode(sid)
                    logging.info(decode1)
                    feature.isLoggedIn = True
                    #logging.info(' ECHOGS: ' + str(sid['expires']))
                    
            if self.request.cookies['EcHogs2']:
                hogs2 = self.request.cookies['EcHogs2']
                if hogs2:
                    decode2 = Cookie.BaseCookie.value_decode(hogs2)
                    logging.info(decode2)
                    expires = hogs2['expires']
                    logging.info('echogs2 : ' + str(expires))
        else:
            feature.isLoggedIn = False
        '''if cook:
            logging.info("GOT COOk")
        cookies = {}
        raw_cookies = self.request.headers.get('Cookies')
        if raw_cookies:
            logging.info(" GOT COOKIES")
            for cookie in raw_cookies.split(";"):
                name, value = cookie.split("=")
                for name, value in cookie.split("="):
                    cookies[name] = value
                    logging.info(cookies[name] + ' = ' + value)
        logging.info("NO COOKIES")  ''' 
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
        logging.info(" IMAGE KEY = " + key)
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



