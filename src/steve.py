'''
Created on Sep 23, 2013

@author: Theo
'''
STEVE_EMAIL = 'stephentriphahn@gmail.com'

import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from model import EmailMessage
from services import forward_email_to_owner

class LogSenderHandler(InboundMailHandler):
    
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        html_bodies = mail_message.bodies()
        
        email_message_body = ''
        for content_type, body in html_bodies:
            decoded_html = body.decode()
            email_message_body = decoded_html + email_message_body
            logging.info("body message: " + decoded_html)
       
        new_steve_email = EmailMessage()
        new_steve_email.populate(sender = mail_message.sender,
                                 subject = mail_message.subject,
                                 owner = 'steve',
                                 message_body = email_message_body)
        new_steve_email.put()    
        
        forward_email_to_owner(STEVE_EMAIL, email_message_body)
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)