from ProductProcesser import *
from ProductReader import *
from Standardizer import *
from SpecsReader import *
from Quantizer import *
from BsonIO import *
from CommonFieldQuantizer import *

def regenerateOutputs(): 
    generateSpecsStatistics()
    preprocessData()

def main():
    #generateFieldsExpandedProducts(printing = False)
    products = readProducts(fileName = 'expandedProducts.bson', decoding = None)

    #generateCommonFieldList(products = products)
    #checkCommonFieldsCount(products)
    #generateCommonFieldStatistics(products)
    #generateCommonFieldsValueMap(products, regenerate = False)
    generateCommonFieldValueLists(products = products,printing = False)
    generateNotNullCommonFieldValueLists(products = products)
    print 'DONE'

main()

