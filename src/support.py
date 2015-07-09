'''
Created on Sep 23, 2013

@author: Theo
'''

'''
Created on Sep 23, 2013

@author: Theo
'''
BRIAN_EMAIL = 'brossetti1@gmail.com'
ANDREW_EMAIL = 'andrewtheobald43@gmail.com'

import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from model import EmailMessage, email_key
from services import forward_email_to_owner
import webapp2


class LogSenderHandler(InboundMailHandler):
    
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        html_bodies = mail_message.bodies()
        
        email_message_body = ''
        for content_type, body in html_bodies:
            decoded_html = body.decode()
            email_message_body = decoded_html + email_message_body
            logging.info("body message: " + decoded_html)
       
        new_support_email = EmailMessage(parent=email_key('Email'))
        new_support_email.populate(sender = mail_message.sender,
                                 subject = mail_message.subject,
                                 owner = 'support',
                                 message_body = email_message_body)
        new_support_email.put()    
        
        forward_email_to_owner(BRIAN_EMAIL, email_message_body)
        forward_email_to_owner(ANDREW_EMAIL, email_message_body)
        logging.info("Fowarding email to Brian and Andrew")
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
        