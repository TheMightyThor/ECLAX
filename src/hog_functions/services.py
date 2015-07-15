'''
Created on Sep 21, 2013

@author: Theo
'''
from google.appengine.api import mail
from hog_models.model import User
import logging

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

def text_all_players(message_body, message_title):
    players = User.all().filter('isPlayer =', True).run()
    logging.info(players)
    attPhoneNumbers = []
    vznPhoneNumbers = []
    tMobilePhoneNumbers = []
    sprintPhoneNumbers = []
    for player in players:
        if player.cell_carrier ==1:
            attPhoneNumbers.append(str(player.cell_number) + '@txt.att.net')
        if player.cell_carrier ==2:
            vznPhoneNumbers.append(str(player.cell_number) + '@vtext.com')
        if player.cell_carrier ==3:
            tMobilePhoneNumbers.append(str(player.cell_number) + '@tmobmail.net')
        if player.cell_carrier ==4:
            sprintPhoneNumbers.append(str(player.cell_number) + '@messaging.sprintpcs.com')
    attEmail = ';'.join(attPhoneNumbers)
    vznEmail = ';'.join(vznPhoneNumbers)
    tMobEmail = ';'.join(tMobilePhoneNumbers)
    sprintEmail = ';'.join(sprintPhoneNumbers)
    emails = attEmail + ';' + vznEmail + ';' + tMobEmail + ';' + sprintEmail
    logging.info(emails)
    email_user(emails, 'All Hogs', message_body, message_title)
    
'''T-Mobile: phonenumber@tmomail.net
Virgin Mobile: phonenumber@vmobl.com
Cingular: phonenumber@cingularme.com
AT&T: phonenumber@txt.att.net
Sprint: phonenumber@messaging.sprintpcs.com
Verizon: phonenumber@vtext.com
Nextel: phonenumber@messaging.nextel.com'''