'''
Created on Jul 9, 2015

@author: Theo
'''

def set_logged_in_cookie(self, key):
        sid = str(key)
        cookie_name = '='.join(('EcHogs',sid))
        self.response.headers.add_header('Set-Cookie',cookie_name)