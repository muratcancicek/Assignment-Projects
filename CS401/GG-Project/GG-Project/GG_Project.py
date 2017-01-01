from ProductProcesser import *
from ProductReader import *
from Standardizer import *
from SpecsReader import *
from Quantizer import *
from BsonIO import *

def regenerateOutputs(): 
    generateSpecsStatistics()
    preprocessData()

def generateCommonFieldStatistics(products = None, printing = False):
    products = readProducts(products, fileName = 'expandedProducts.bson')
    generateCommonFieldList(products = products, printing = True)
    generateCommonFieldValueLists(products = products, printing = True)
    generateCommonFieldValueTypes(products = products, printing = True)
    generateCommonFieldValueSets(products = products, printing = True)
    generateCommonFieldValueTypeCounts(products = products, printing = True)

def main(): 
    #generateFieldsExpandedProducts(printing = True)
    generateCommonFieldStatistics()

main()

