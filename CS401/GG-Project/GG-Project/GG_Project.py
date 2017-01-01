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
    generateCommonFieldList(products = products, printing = printing)
    generateCommonFieldValueLists(products = products, printing = printing)
    generateCommonFieldValueTypes(products = products, printing = printing)
    generateCommonFieldValueSets(products = products, printing = printing)
    generateCommonFieldValueCounts(products = products, printing = printing)
    generateCommonFieldValueTypeCounts(products = products, printing = printing)

def main():
    #generateFieldsExpandedProducts(printing = False)
    products = readProducts(fileName = 'expandedProducts.bson')
    #checkCommonFieldsCount(products)
    generateCommonFieldStatistics(products)

main()

