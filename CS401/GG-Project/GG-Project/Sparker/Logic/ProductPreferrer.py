from Sparker.SparkLogProcesser.SparkLogAnalyzer import *
from Sparker.SparkLogProcesser.SparkLogOperator import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from MainSrc.PythonVersionHandler import *
from Sparker.PySparkImports import *

def getListedIdsFromJourney(journey):
    searches = journey.filter(isSearchLog)
    def extender(a, b): a.extend(b); return a
    ids = searches.map(lambda log: log['ids'] if 'ids' in log else []).reduce(extender)
    return ids

def getLoggedIds(journey, module):
    interestingLogs = sortedLogs(journey.filter(lambda log: log['module'] == module))
    return interestingLogs.map(lambda log: log['id'])#.collect()

def modulizeIds(journey):
    productLogs = journey.filter(isProductLog)
    paidProducts = getLoggedIds(productLogs, 'payment')
    cartProducts = getLoggedIds(productLogs, 'cart')
    clickedProducts = getLoggedIds(productLogs, 'item')
    print_(paidProducts.count(), cartProducts.count(), clickedProducts.count()) 
    printActions(productLogs.filter(lambda log: log['module'] == 'cart'))
    interestingIds = paidProducts.union(cartProducts).union(clickedProducts)
    cartProducts.show()

def getInterestingIds(journey): 
    print_(journey.count())
    #ids = getListedIdsFromJourney(journey)
    ##productLogs.filter(lambda log: log['id'] in clickedProducts).foreach(print_)
    #modulizeIds(journey)
    #print_(ids)