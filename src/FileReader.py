'''
Created on Mar 31, 2014

@author: Theo
'''
import csv


with open('C:\Users\Theo\workspace\CogentWeb\src\TemplateInterchangeData.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print ', '.join(row)
    