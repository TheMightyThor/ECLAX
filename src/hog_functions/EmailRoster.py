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
        sender = mail_message.sender
        cleanMail = sender.partition('<')[2].partition('>')[0]
        cleanSubject = mail_message.subject.partition(':')
        logging.info("cleanMail = " +cleanMail)
        user = User.all().filter('email =', cleanMail).get()
        eventName = cleanSubject[2].lstrip().rstrip()
        plainTextBody = mail_message.bodies('text/plain')
        logging.info(eventName)
        gEvent = GameEvent.all().filter('name =', eventName).get()
        
        if user is not None and gEvent is not None:
            logging.info('user is not none and gevent is not none')
            for content_type, body in plainTextBody:        
                decoded_msg_body = body.decode()
                decoded_msg_body.lstrip()
                playing = decoded_msg_body[0].lower()
                 
                if playing is not None and playing == 'y':                  
                    if any(str(user.key()) in s for s in gEvent.outRoster):
                        i = gEvent.outRoster.index(str(user.key()))
                        del gEvent.outRoster[i]
                        
                    if not any(str(user.key()) in s for s in gEvent.roster):
                        gEvent.roster.append(str(user.key()))
                    gEvent.put()
                if playing is not None and playing == 'n':
                    if any(str(user.key()) in s for s in gEvent.roster):
                        i = gEvent.roster.index(str(user.key()))
                        del gEvent.roster[i]
                        
                    if not any(str(user.key()) in s for s in gEvent.outRoster):        
                        gEvent.outRoster.append(str(user.key()))
                    gEvent.put()
        else:
            for content_type, body in plainTextBody:        
                decoded_msg_body = body.decode()
                logging.error('Email from = ' + mail_message.sender + ' had an error' + ' Subject = ' + mail_message.subject +' Message body = ' + decoded_msg_body)      
                
        
app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)