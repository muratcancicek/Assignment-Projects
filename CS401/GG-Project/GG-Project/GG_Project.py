from CommonFieldQuantizer import *
from FirstTermMethods import *
from ProductProcesser import *
from VectorGenerator import *
from ProductReader import *
from BsonIO import *
a = 66
def main(b = a+4): 
    #c = evalBson('categories.bson')
    #print c
    c = b
    print evalBson('data/commonFieldStatistics/values/commonFieldValueMap.bson')
    print readCommonFieldValueMap()
    #learnCategories()
    print 'DONE'


main()