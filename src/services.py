'''
Created on Sep 21, 2013

@author: Theo
'''
from google.appengine.api import mail



def __cleanString__(string):
    
    test = ''

    cleanstring = string.replace(';',test).replace("'", test)
    
    return cleanstring


def email_user(email_address, user_name, message, subject):
    
    mail.send_mail(sender="East Cobb Hedgehogs <EastCobbHedgehogs@gmail.com>",
                   to = email_address,
                   subject = subject,
                   body = message)

