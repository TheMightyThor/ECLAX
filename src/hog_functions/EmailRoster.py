'''
Created on Jul 19, 2015

@author: Theo
'''
import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from email.iterators import body_line_iterator
from hog_models.GameEvent import GameEvent
from hog_models.UserManagement import User
import email

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender + ' ' + mail_message.subject)        
        
        cleanSubject = mail_message.subject.partition(':')
        
        user = User.all().filter('email =', mail_message.sender).get()
        eventName = cleanSubject[2].lstrip().rstrip()
        plainTextBody = mail_message.bodies('text/plain')
        
        gEvent = GameEvent.all().filter('name =', eventName).get()
        
        if gEvent is not None:
            logging.info(str(gEvent.name))
        
        if user is None:
            sender = str(mail_message.sender)
            cellEmail = sender.partition('@')           
            user = User.all().filter('cell_number =', cellEmail[0])
        if user is not None and gEvent is not None:
            for content_type, body in plainTextBody:        
                decoded_msg_body = body.decode()
                decoded_msg_body.lstrip()
                playing = decoded_msg_body[0].lower()
                 
                if playing is not None and playing == 'y':
                    if gEvent.roster:
                        gEvent.roster = [str(user.key())]
                    else:
                        gEvent.roster.append(str(user.key()))
                        gEvent.put()
                if playing is not None and playing == 'n':
                    if gEvent.outRoster is None:
                        gEvent.outRoster = [str(user.key())]
                    else:
                        gEvent.outRoster.append(str(user.key()))
                        gEvent.put()
        else:
            logging.error('Email from = ' + mail_message.sender + ' had an error')        
                
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)