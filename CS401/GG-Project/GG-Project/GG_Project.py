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
    #generateCommonFieldList(printing = True)
    #generateCommonFieldValueLists(printing = True)
    #generateCommonFieldValueTypes(printing = True)
    #generateCommonFieldValueSets(printing = True)
    generateCommonFieldValueTypeCounts(printing = True)

main()

