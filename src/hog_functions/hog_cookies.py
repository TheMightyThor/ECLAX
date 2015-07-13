'''
Created on Jul 9, 2015

@author: Theo
'''

import logging
import os
from __builtin__ import False

def set_logged_in_cookie(self, key):
        sid = str(key)
        cookie_name = '='.join(('EcHogs',sid))
        self.response.headers.add_header('Set-Cookie',cookie_name)
        
def get_logged_in_cookie(self):
    
    logging.info('Finding Cookies')
    try:
        if self.request.cookies is not None:
            if self.request.cookies['EcHogs'] is not None:
                sid =  self.request.cookies['EcHogs']
                if sid is not None:
                    return True
                else:
                    logging.info('sid is none')
                    return False        
                           
            else:
                logging.info('Found cookies but did not find EcHogs')
                return False
        else:
            logging.info('No cookies')
            return False
    except:
        logging.exception(os.sys.exc_info()[0])
        return False
    
    
def get_logged_in_cookie_user_id(self):
    
    logging.info('Finding Cookies')
    try:
        if self.request.cookies is not None:
            if self.request.cookies['EcHogs'] is not None:
                logging.info(self.request.cookies)
                sid =  self.request.cookies['EcHogs']
                if sid is not None:
                    logging.info("SID = " + str(sid))
                    return sid
                else:
                    logging.info('sid is none')
                    return None        
                           
            else:
                logging.info('Found cookies but did not find EcHogs')
                return None
        else:
            logging.info('No cookies')
            return None
    except:
        logging.exception(os.sys.exc_info()[0])
        return None  