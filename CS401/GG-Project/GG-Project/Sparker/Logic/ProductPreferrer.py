from Sparker.SparkLogProcesser.SparkLogAnalyzer import *
from Sparker.SparkLogProcesser.SparkLogOperator import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from MainSrc.PythonVersionHandler import *
from Sparker.PySparkImports import *

def getListedIdsFromJourney(journey):
    searches = journey.filter(isSearchLog)
    def extender(a, b): a.extend(b); return a
    ids = searches.map(lambda log: (log['ids'] if log['ids'] != None else []) if 'ids' in log else []).reduce(extender)
    return ids#sc_().parallelize().distinct()#unique()

def getLoggedIds(journey, module):
    interestingLogs = sortedLogs(journey.filter(lambda log: log['module'] == module))
    return interestingLogs.map(lambda log: (log['id']))

def printActionsByModule(logs, module):
    printActions(logs.filter(lambda log: log['module'] == module))

def summaryIds(ids):
    print_(ids['paid'].count(), ids['cart'].count(), ids['clicked'].count())# ids['listed'].count(), 
    print_(ids['paid'].collect())
    print_(ids['cart'].collect())
    print_(ids['clicked'].collect())

def cleanIds(ids):
    s = ids['listed']#.map(lambda id: (id, id))
    #ids['paid'] = ids['paid'].filter(lambda l: l in s)
    ids['cart'] = ids['cart'].subtractByKey(ids['paid'])
    ids['clicked'] = ids['clicked'].subtractByKey(ids['paid']).subtractByKey(ids['cart'])
    return ids 
    #ids['paid'] = ids['paid'].filter(lambda l: l in s)
    #ids['cart'] = ids['cart'].filter(lambda l: l in s).subtractByKey(ids['paid'])
    #ids['clicked'] = ids['clicked'].filter(lambda l: l in s).subtractByKey(ids['paid']).subtractByKey(ids['cart'])
    #return ids 

def countIds(ids):
    for process in ['paid', 'cart', 'clicked']:
        ids[process] =  sc_().parallelize(ids[process].countByValue().items())
    return ids

def modulizeIds(journey):
    productLogs = journey.filter(isProductLog)
    ids = { 
    'listed': getListedIdsFromJourney(journey),
    'paid': getLoggedIds(productLogs, 'payment'),
    'cart': getLoggedIds(productLogs, 'cart'),
    'clicked': getLoggedIds(productLogs, 'item') }
    #summaryIds(ids)
    ids = countIds(ids)
    summaryIds(ids)
    ids = cleanIds(ids)
    summaryIds(ids)
    return ids

def keyPairIds(id1, id2):
    return str(id1) + '_' + str(id2)

positive = 1
negative = -1
def labelByValues(v1, v2):
    return positive if v1 >= v2 else negative

def getLabeledPairs(journey):
    ids = modulizeIds(journey)
    ids['paid'] = ids['paid'].toLocalIterator()
    ids['cart'] = ids['cart'].toLocalIterator()
    ids['clicked'] = ids['clicked'].toLocalIterator()
    print_(ids['cart'])
    labeledPairs = []
    def addPairByValue(id1, id2, v1, v2): 
        if id1 != id2:
            labeledPairs[keyPairIds(id1, id2)] = labelByValues(v1, v2)
            labeledPairs[keyPairIds(id2, id1)] = labelByValues(v2, v1)

    def addDominantPair(id1, id2): 
        if id1 != id2:
            labeledPairs[keyPairIds(id1, id2)] = positive
            labeledPairs[keyPairIds(id2, id1)] = negative

    for paidId, pCount in ids['paid']:
        for paidId2, pCount2 in ids['paid']:
             addPairByValue(paidId, paidId2, pCount, pCount2)
        for cartId, cartCount in ids['cart']:
             addDominantPair(paidId, cartId)
        for clickedId, clickedCount in ids['clicked']:
             addDominantPair(paidId, clickedId)
             
    for cartId, cartCount in ids['cart']:
        for cartId2, cartCount2 in ids['cart']:
             addPairByValue(cartId, cartId2, cartCount, cartCount2)
        for clickedId, clickedCount in ids['clicked']:
             addDominantPair(cartId, clickedId)
             
    for clickedId, clickedCount in ids['clicked']:
        for clickedId2, clickedCount2 in ids['clicked']:
             addPairByValue(clickedId, clickedId2, clickedCount, clickedCount2)
    #labeledPairs.saveAsTextFile('hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/data/part0&1_iphone_6')
    return labeledPairs

def getInterestingIds(journey): 
    labeledPairs = getLabeledPairs(journey)
    print_(labeledPairs)
    return labeledPairs