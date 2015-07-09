'''
Created on Apr 6, 2014

@author: Theo
'''
import os

from DataQuery import DB__deleteAllMccData, DB__populateDbWithMCCCodeData, DB__selectAllMCCCodes, DB__selectMccCode
from csvImport import getCsvData
import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])
   
MODELS = ['MCCData',
          'Relations']

DATABASE_TRANSACTIONS = ['ImportCSV',
                         'DeleteAll',
                         'DeleteOne',
                         'SelectAll']
                         
class DeleteAll(webapp2.RequestHandler):
   
    
    def get(self):
     
     
        template_values = {
                           'transactions' : DATABASE_TRANSACTIONS,
                           'models' : MODELS,
                           }
        template = JINJA_ENVIRONMENT.get_template('html/database.html')
        self.response.write(template.render(template_values))
        
       
    def post(self):
       
        resp_trans = self.request.get('transactions')
        resp_model = self.request.get('models')
        result = formSelectionToQuery(resp_model, resp_trans)
        template_values = {
                           'transactions' : DATABASE_TRANSACTIONS,
                           'models' : MODELS,
                           'results': result,
                           }
        
        template = JINJA_ENVIRONMENT.get_template('html/database.html')
        self.response.write(template.render(template_values))
        
def formSelectionToQuery(model, transaction):
    
    if transaction.__eq__('ImportCSV'):
        return getCsvData()
    if transaction.__eq__('DeleteAll'):
        return DB__deleteAllMccData()
        
app = webapp2.WSGIApplication([('/database/', DeleteAll),
                               ], debug=True)
