'''
Created on Apr 6, 2014

@author: Theo
'''
import csv
from model import MCCData
import logging
from services import __cleanString__
import os

fn = os.path.join(os.path.dirname(__file__), 'TemplateInterchangeData3.csv')
class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
def getCsvData():
        logging.info("Getting CSV data from ")
        '''with open('C:\Users\Theo\workspace\CogentWeb\src\TemplateInterchangeData3.csv') as csvfile:'''
        with open(fn) as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            
            spamreader = csv.reader(csvfile, dialect, delimiter=',', quotechar='|')
            
            rows = []
            counter = 0
            for row in spamreader:
                
                if row.__len__() >= 6:
                    
                    cleanexcelrow = MCCData()
                    
                    if row[0] is None:
                        cleanexcelrow.mccCode = 'rizo is lame'
                    else:
                        cleanexcelrow.mccCode = __cleanString__(row[0])
                        
                    if row[1] is None:
                        cleanexcelrow.category = 'rizo is super lame'
                    else:
                        cleanexcelrow.category =  __cleanString__(row[1])
                        
                    if row[2] is None:
                        cleanexcelrow.percentVol = 0.0
                    else:
                        cleanexcelrow.percentVol = float( __cleanString__(row[2]))
                    
                    if row[3] is None:
                        cleanexcelrow.percentCount = 0.0
                    else:
                        cleanexcelrow.percentCount = float( __cleanString__(row[3]))
                    
                    if row[4] is None:
                        cleanexcelrow.rate = 0.0
                    else:
                        cleanexcelrow.rate = float( __cleanString__(row[4]))
                    
                    if row[5] is None:
                        cleanexcelrow.transactionFee = 0.0
                    else:
                        cleanexcelrow.transactionFee = float(__cleanString__(row[5]))
                        
                    rows.append(cleanexcelrow)
                    counter = counter + 1 
                    
                else:
                    logging.info('Skipped ' + str(counter) )
                    
            return rows