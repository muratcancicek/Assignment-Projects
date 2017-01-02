from ProductProcesser import *
from ProductReader import *
from Standardizer import *
from SpecsReader import *
from Quantizer import *
from BsonIO import *

def regenerateOutputs(): 
    generateSpecsStatistics()
    preprocessData()
def main():
    generateFieldsExpandedProducts(printing = False)
    products = readProducts(fileName = 'expandedProducts.bson', decoding = None)
    checkCommonFieldsCount(products)
    generateCommonFieldStatistics(products)
    print 'DONE'

main()

