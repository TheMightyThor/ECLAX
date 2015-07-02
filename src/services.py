'''
Created on Sep 21, 2013

@author: Theo
'''
from google.appengine.api import mail
import logging


def __cleanString__(string):
    
    test = ''

    cleanstring = string.replace(';',test).replace("'", test)
    
    return cleanstring

Dfault_email = 'andrewtheobald43@gmail.com'

Dfault_name = 'Nukka'
  
def email_after_login(email_address, user_name):
    
    mail.send_mail(sender="Andrew Theobald <andrewtheobald43@gmail.com>",
                  to= email_address,
                  subject="Thanks For Stopping By",
                  body="""
Dear """ + user_name + """,

Thanks for checking out the site.  Feel free to provide suggestions.

-Andrew

***THIS EMAIL WAS AUTO GENERATED***
""")

def forward_email_to_owner(to_owner, email_message):
    
    mail.send_mail(sender = "CogentTestApp <support@cogenttestapp.appspotmail.com>", 
                   to = to_owner,
                   subject = "Getting Some FeedBack",
                   body = email_message)
    logging.info("Message Sent! to " + to_owner)
