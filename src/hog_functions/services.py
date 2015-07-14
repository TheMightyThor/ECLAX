'''
Created on Sep 21, 2013

@author: Theo
'''
from google.appengine.api import mail
from hog_models.model import User


def is_player_from_header(self):
    if self.request.cookies:
        if self.request.cookies['EcHogs']:
            sid =  self.request.cookies['EcHogs']
            if sid:
                user = User.get(sid)
                if user:
                    return user.isPlayer
    else:
        return False    

def __cleanString__(string):
    
    test = ''

    cleanstring = string.replace(';',test).replace("'", test)
    
    return cleanstring

def get_cookie(self,name,default=None):
    """Gets the value of the cookie with the given name,else default."""
    if name in self.request.cookies:
        return self.request.cookies[name]
    return default

def set_cookie(self,name,value,domain=None,expires=None,path="/",expires_days=None):
    """Sets the given cookie name/value with the given options."""



    new_cookie = Cookie.BaseCookie()
    new_cookie[name] = value
    if domain:
        new_cookie[name]["domain"] = domain
    if expires_days is not None and not expires:
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=expires_days)
    if expires:
        timestamp = calendar.timegm(expires.utctimetuple())
        new_cookie[name]["expires"] = email.utils.formatdate(timestamp,localtime=False,usegmt=True)
    if path:
        new_cookie[name]["path"] = path
    for morsel in new_cookie.values():
        self.response.headers.add_header('Set-Cookie',morsel.OutputString(None))

def email_user(email_address, user_name, message, subject):
    
    mail.send_mail(sender="East Cobb Hedgehogs <EastCobbHedgehogs@gmail.com>",
                   to = email_address,
                   subject = subject,
                   body = message)

'''T-Mobile: phonenumber@tmomail.net
Virgin Mobile: phonenumber@vmobl.com
Cingular: phonenumber@cingularme.com
AT&T: phonenumber@txt.att.net
Sprint: phonenumber@messaging.sprintpcs.com
Verizon: phonenumber@vtext.com
Nextel: phonenumber@messaging.nextel.com'''