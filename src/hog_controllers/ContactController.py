'''
Created on Jul 6, 2015

@author: Theo
'''
import logging
import os

import jinja2
from hog_models.model import Message, Feature, User
from hog_functions import services
import webapp2


RECUITER_EMAILS = ['andrewtheobald43@gmail.com','marshallhood@gmail.com','stdockery@gmail.com',]

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join( os.path.dirname ( __file__), os.path.pardir)),
    extensions=['jinja2.ext.autoescape'])


class Contact(webapp2.RequestHandler):
    
    def get(self):
        
        template = JINJA_ENVIRONMENT.get_template('html/contact.html')   
        self.response.write(template.render())
        
    def post(self):
        contactName = self.request.get('recuit_name')
        ncaa = self.request.get('ncaa')
        if ncaa:
            playedNcaa = 'yes'
        else:
            playedNcaa = 'no'
        mcla = self.request.get('mcla')
        if mcla:
            playedMcla = 'yes'
        else:
            playedMcla = 'no'
        pos = self.request.get('pos')
        age = self.request.get('age')
        city = self.request.get('city')
        email = self.request.get('email')
        phone = self.request.get('phone')
        
        message = 'Got a new guy looking into the club.\nName = {}\nNcaa = {}\nMCLA = {}\nPosition = {}\nAge = {}\nCity = {}\nEmail = {}\nPhone = {}\n**************AUTO GENERATED EMAIL CONTACT PLAYER DIRECTLY *************'.format(contactName,
                                                                                                                                                                                                         playedNcaa,
                                                                                                                                                                                                         playedMcla,
                                                                                                                                                                                                         pos,
                                                                                                                                                                                                         age,
                                                                                                                                                                                                         city,
                                                                                                                                                                                                         email,
                                                                                                                                                                                                         phone
                                                                                                                                                                                                          )
        
        logging.info(message.__str__())
        title = 'New Contact'
        for email in RECUITER_EMAILS:
            services.email_user(email, email, message, title)
        
        self.redirect('/index')
        
app = webapp2.WSGIApplication([                                     
                                       ('/contact/', Contact),
                                       ('/contact/contactmessage', Contact),                                      
                                       ], debug=True)
