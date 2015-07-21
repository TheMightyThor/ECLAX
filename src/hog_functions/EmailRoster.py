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
        logging.info(eventName)
        gEvent = GameEvent.all().filter('name =', eventName).get()
        
        if gEvent is not None:
            logging.info(str(gEvent.name))
        
        if user is None:
            logging.info('User was none from email')
            sender = str(mail_message.sender)
            cellEmail = sender.partition('@')           
            user = User.all().filter('cell_number =', cellEmail[0])
        if user is not None and gEvent is not None:
            logging.info('user is not none and gevent is not none')
            for content_type, body in plainTextBody:        
                decoded_msg_body = body.decode()
                decoded_msg_body.lstrip()
                playing = decoded_msg_body[0].lower()
                 
                if playing is not None and playing == 'y':
                    logging.info('playing is not none and is y')
                    if gEvent.roster is None:
                        logging.info('roster is none')
                        gEvent.roster = [str(user.key())]
                    else:
                        logging.info('roster is not none adding player')
                        gEvent.roster.append(str(user.key()))
                        gEvent.put()
                if playing is not None and playing == 'n':
                    logging.info('playing is not none and playing is n')
                    if gEvent.outRoster is None:
                        logging.info('out roster is none adding roster and player')
                        gEvent.outRoster = [str(user.key())]
                    else:
                        logging.info('out roster is not none adding just player')
                        gEvent.outRoster.append(str(user.key()))
                        gEvent.put()
        else:
            logging.error('Email from = ' + mail_message.sender + ' had an error')        
                
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)