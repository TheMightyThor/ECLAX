'''
Created on Apr 6, 2014

@author: Theo
'''
import logging
from google.appengine.ext import ndb 
from model import mccdata_key, MCCData

def DB_selectAllDataOfMCCCodeType():
    q = MCCData.query(MCCData.mccCode == '742').get()
    rows = q.fetch()       
    return rows

def DB_selectAllCategories():
    q = MCCData.query(projection=[MCCData.category], distinct=True)
    rows = q.fetch()
    result = []
    for row in rows:
        result.append(row.category)
    return result
        
def DB__selectAllMCCCodes():
    
    logging.info('Starting DB__selectAllMCCCodes')
    
    mcc_query = MCCData.query(
            ancestor=mccdata_key('MccData'))
    codes = mcc_query.fetch()
    
    length = str(codes.__len__())
                 
    logging.info('Returned list with ' + length + ' rows' )
                 
    return codes

        
def DB__populateDbWithMCCCodeData(mccRow):
        
        logging.info('Starting __populateDbWithMCCCodeData Category: ' + mccRow.category + ' MCCCode: '  + mccRow.mccCode)
        
        new_mccdata = MCCData()
        new_mccdata.populate(mccCode = mccRow.mccCode,
                                     category = mccRow.category,
                                     percentVol = mccRow.percentVol,
                                     percentCount = mccRow.percentCount,
                                     rate = mccRow.rate,
                                     transactionFee = mccRow.transactionFee,
                                     )
        new_mccdata.put()

def DB__deleteAllMccData():
    
    number_of_iterations = 0
   
    ndb.delete_multi(MCCData.query().fetch(keys_only=True))
        
    number_deleted = str(number_of_iterations * 1000)    
    logging.info('Deleted roughly ' + number_deleted)
    
    return number_deleted

def DB__selectMccCode(mccCode):
    
    qry = MCCData.query(MCCData.mccCode == mccCode)
    
    result = qry.fetch()
    
    return result
    