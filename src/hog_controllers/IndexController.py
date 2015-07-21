import datetime
import logging
import os

import jinja2
from hog_models.model import Message, Picture, Feature
from hog_models.UserManagement import PlayerInfo, User
from hog_models.GameEvent import GameEvent
import webapp2
import security
from hog_functions import hog_cookies


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join( os.path.dirname ( __file__), os.path.pardir)),
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
        newUser.isAdmin = False
        newUser.email = self.request.get('email')
        exist = User.all().filter('email', newUser.email).get()
        if exist:
            self.response.write('Email already exists')
        else:
            newUser.username = self.request.get('user_name')
            pw = self.request.get('password')
            newUser.password = security.generate_password_hash(pw, method='sha1', length=22, pepper='3cH06')
            player_password = self.request.get('player_password')
            newUser.cell_number = int(self.request.get('cell_number'))
            
            newUser.cell_carrier  = int(self.request.get('cell_carrier'))
            logging.info(player_password)
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
        authUser = User.all().filter('username =', user.username).get()
        if authUser is not None:
            key = authUser.key()
            pwHash = security.check_password_hash(password, authUser.password, '3cH06')
            if pwHash:
                hog_cookies.set_logged_in_cookie(self, str(key))
                
                self.redirect('/'+ redirect)
            else:
                self.response.write('Incorrect password')
        else:
            self.response.write('User does not exist')
            
class MainPage(webapp2.RequestHandler):
    
    def post(self):
        feature = Feature()            
        userKey = hog_cookies.get_logged_in_cookie_user_id(self)
        authuser = User.get(userKey)
        feature.isAdmin = authuser.isAdmin
        template_values = {
                           'feature', feature
          
        }
        
        template = JINJA_ENVIRONMENT.get_template('/html/index.html')
        self.response.write(template.render(template_values))
        
        
                                                    
    def get(self):
        feature = Feature()
        feature.isLoggedIn = hog_cookies.get_logged_in_cookie(self)
        user_key = hog_cookies.get_logged_in_cookie_user_id(self)
        if user_key is not None:
            user = User.get(user_key)
            if user is not None:
                feature.isPlayer = user.isPlayer
                feature.isAdmin = user.isAdmin
                
            else:
                feature.isPlayer = False
        else:
            feature.isPlayer = False
                
        now = datetime.date.today()
        events = GameEvent.all().run()
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
        
        template = JINJA_ENVIRONMENT.get_template( "/html/index.html")
         
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
        
    
application = webapp2.WSGIApplication([
                                       ('/', MainPage),
                                       ('/login', LogIn),
                                       ('/gallery', Gallery),
                                       ('/index', MainPage),
                                       ('/newuser', NewUser),
                                       ('/index/postimage', PostImage),
                                       ('/img', Image),                            
                                        ], debug=True)



