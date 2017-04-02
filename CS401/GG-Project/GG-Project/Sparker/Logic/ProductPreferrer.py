from Sparker.SparkLogProcesser.SparkLogOperator import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogAnalyzer import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from MainSrc.PythonVersionHandler import *
from Sparker.PySparkImports import *
import Sparker.SparkLogProcesser.SparkLogAnalyzer as SLA

def printActionsByModule(logs, module):
    printActions(logs.filter(lambda log: log['module'] == module))

def getListedIdsFromJourney(journey):
    searches = journey.filter(SLA.isSearchLog)
    return getIdsFromSearches(searches)

def getLoggedIds(journey, module):
    interestingLogs = journey.filter(lambda log: log['module'] == module).sortBy(lambda log: log['timestamp'])
    return interestingLogs.map(lambda log:log['id'] )
#(, log['timestamp'])
def countIds(ids):
    for process in ['paid', 'cart', 'clicked']:
        ids[process+'Cnt'] =  sc_().parallelize(ids[process].countByValue().items())
    ids['listedCnt'] = sc_().parallelize(sc_().parallelize([id for id in ids['listed']]).countByValue().items())
    return ids

def summaryIds(ids):
    print_('Listed counts =', ids['listedCnt'].count(), 'Paid counts =', ids['paidCnt'].count(), 
           'Cart counts =', ids['cartCnt'].count(), 'Clicked counts =', ids['clickedCnt'].count())
    
def cleanCount(ids):
    def clearUnListedIds(rdd):
        return rdd.subtractByKey(ids['listedCnt'].subtractByKey(rdd))
    ids['paidCnt'] = clearUnListedIds(ids['paidCnt'])
    ids['cartCnt'] = clearUnListedIds(ids['cartCnt']).subtractByKey(ids['paidCnt'])
    ids['clickedCnt'] = clearUnListedIds(ids['clickedCnt']).subtractByKey(ids['paidCnt']).subtractByKey(ids['cartCnt'])
    return ids 

def modulizeIds(journey):
    productLogs = journey.filter(isProductLog)
    ids = { 
    'listed': getListedIdsFromJourney(journey),
    'paid': getLoggedIds(productLogs, 'payment'),
    'cart': getLoggedIds(productLogs, 'cart'),
    'clicked': getLoggedIds(productLogs, 'item') }
    ids = countIds(ids)
    summaryIds(ids)
    ids = cleanCount(ids)
    summaryIds(ids)
    return ids

def keyPairIds(id1, id2):
    return str(id1) + '_' + str(id2)

positive = 1
negative = -1

def getLabeledPairsWithModulizedIds(journey):
    ids = modulizeIds(journey)
    paidCnt = ids['paidCnt'].collect()
    cartCnt = ids['cartCnt'].collect()
    clickedCnt = ids['clickedCnt'].collect()
    listedCnt = ids['listedCnt'].collect()
    clickedIds = [id for id, v in clickedCnt]
    levels = [paidCnt, cartCnt, clickedCnt, listedCnt]
    labeledPairs = {}

    def addDominantPair(id1, id2): 
        if id1 != id2:
            labeledPairs[keyPairIds(id1, id2)] = positive
            labeledPairs[keyPairIds(id2, id1)] = negative

    def labelByValues(v1, v2):
        return positive if v1 > v2 else negative

    def labelBySubValues(id1, id2, level):
        if id1 == id2: 
            return
        elif level == len(levels):
            v1 = clickedIds.index(id1) if id1 in clickedIds else -1
            v2 = clickedIds.index(id2) if id1 in clickedIds else -1
            if v1 == v2:
                addDominantPair(id1, id2)
            else:
                addPairByValue(id1, id2, v1, v2, level)
        else:
            cnts = levels[level]  
            v1, v2 = None, None
            for id, v in cnts:
                if id == id1: v1 = v
                if id == id2: v2 = v
            if v1 == None:
                if v2 == None:
                    labelBySubValues(id1, id2, level + 1)
                else:   
                    addPairByValue(id1, id2, -1, v2, level)
            elif v2 == None:
                addPairByValue(id1, id2, v1, -1, level)
            else:
                addPairByValue(id1, id2, v1, v2, level)

    def addPairByValue(id1, id2, v1, v2, level):
        if id1 != id2: 
            if v1 == v2: 
                labelBySubValues(id1, id2, level + 1)
            labeledPairs[keyPairIds(id1, id2)] = labelByValues(v1, v2)
            labeledPairs[keyPairIds(id2, id1)] = labelByValues(v2, v1)

    for paidId, pCount in paidCnt:
        for paidId2, pCount2 in paidCnt:
             addPairByValue(paidId, paidId2, pCount, pCount2, level = 0)
        for cartId, cartCount in cartCnt:
             addDominantPair(paidId, cartId)
        for clickedId, clickedCount in clickedCnt:
             addDominantPair(paidId, clickedId)
             
    for cartId, cartCount in cartCnt:
        for cartId2, cartCount2 in cartCnt:
             addPairByValue(cartId, cartId2, cartCount, cartCount2, level = 1)
        for clickedId, clickedCount in clickedCnt:
             addDominantPair(cartId, clickedId)
             
    for clickedId, clickedCount in clickedCnt:
        for clickedId2, clickedCount2 in clickedCnt:
             addPairByValue(clickedId, clickedId2, clickedCount, clickedCount2, level = 2)
    ids['labeledPairs'] = sc_().parallelize([(key, v) for key, v in labeledPairs.items()])
    print_(ids['labeledPairs'].count(), ' labeled pairs has been generated by', nowStr())
    return ids