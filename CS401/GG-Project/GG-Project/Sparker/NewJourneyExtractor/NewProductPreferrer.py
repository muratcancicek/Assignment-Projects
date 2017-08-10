from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.NewJourneyExtractor.SearchExtractor import *
from LogProcesser.scalaToPython.python_codes.LumberjackConstants import *
from Sparker.NewJourneyExtractor.Sessionizer import *

KEY_PREFERRED_ID_LIST ='preferred_ids'
KEY_PRODUCT_COEFFICIENT = 1
KEY_CART_COEFFICIENT = 5
KEY_PAYMENT_COEFFICIENT = 10

def findProductIdOnSearches(currentLog, previousJourney):
    lastSearchIndexWithId, productIndex = -1, -1
    previousJourney.reverse()
    count = -1
    for pl in previousJourney:
        if LA.isSearchLog(pl):
            count += 1
            if isinstance(currentLog[KEY_ID], int):
                for t, jd in enumerate(pl[KEY_ID_LIST]):
                    if currentLog[KEY_ID] == jd:
                        return count, t
            elif isinstance(currentLog[KEY_ID], str):
                if '%7C' in currentLog[KEY_ID]:
                    processedIds = [int(i) for i in currentLog[KEY_ID].split('%7C')]
                    for t, jd in enumerate(pl[KEY_ID_LIST]):
                        if jd in processedIds:
                            return count, t
    return lastSearchIndexWithId, productIndex 

def specificPreviousSearches(productLog, search):
    if search[KEY_TIMESTAMP] < productLog[KEY_TIMESTAMP]:
        for id in productLog[KEY_FOUR_IDS]:
            if id in search[KEY_FOUR_IDS]:
                return True
    return False

def specificPreviousSearchesWithId(productLog, search):
    onSearch = False
    if isinstance(productLog[KEY_ID], int):
        if productLog[KEY_ID] in search[KEY_ID_LIST]:
            onSearch = True
    elif isinstance(productLog[KEY_ID], str):
        if '%7C' in productLog[KEY_ID]:
            processedIds = [int(i) for i in productLog[KEY_ID].split('%7C')]
            for id in processedIds:
                if id in search[KEY_ID_LIST]:
                    onSearch = True
                    break
    return onSearch

def findViewedProductIstancesOnSearches(productLog, searches):
    searches = searches.filter(lambda search: specificPreviousSearches(productLog, search)) \
                    .filter(lambda search: specificPreviousSearchesWithId(productLog, search))
    instances = []
    if searches.count() > 0:
        search = searches.sortBy(lambda search: search[KEY_TIMESTAMP], ascending = False).first()
        for i, id in enumerate(search[KEY_ID_LIST]):
            if isinstance(productLog[KEY_ID], int):
                if productLog[KEY_ID] == id:
                    if i > 0:
                        productLog[KEY_PREFERRED_ID_LIST] = search[KEY_ID_LIST][:i]
                        instances.append(productLog)
                        break
            elif isinstance(productLog[KEY_ID], str):
                if '%7C' in productLog[KEY_ID]:
                    processedIds = [int(i) for i in productLog[KEY_ID].split('%7C')]
                    for pid in processedIds:
                        for i, id in enumerate(search[KEY_ID_LIST]):  
                            if pid == id:
                                if i > 0:
                                    productLog[KEY_ID] = pid
                                    productLog[KEY_PREFERRED_ID_LIST] = search[KEY_ID_LIST][:i]
                                    instances.append(productLog)
                                    break
    return instances

def idsMatched(productLog, viewIstance):
    if isinstance(productLog[KEY_ID], int):
        return viewIstance[KEY_ID] == productLog[KEY_ID]
    elif isinstance(productLog[KEY_ID], str):
        return str(viewIstance[KEY_ID]) in productLog[KEY_ID]

def specificPreviousViews(productLog, viewIstance):
    if idsMatched(productLog, viewIstance) and viewIstance[KEY_TIMESTAMP] < productLog[KEY_TIMESTAMP]:
            for id in productLog[KEY_FOUR_IDS]:
                if id in viewIstance[KEY_FOUR_IDS]:
                    return True
    return False

def findcartedOrPaidProductIstancesOnViews(productLog, viewedProductIstances):
    viewedIstances = [instance for instance in viewedProductIstances if specificPreviousViews(productLog, instance)]
    if len(viewedIstances) > 0:
        if productLog[KEY_MODULE] == KEY_MODULE_CART:
            coefficient = KEY_CART_COEFFICIENT
        if productLog[KEY_MODULE] == KEY_MODULE_PAYMENT:
            coefficient = KEY_PAYMENT_COEFFICIENT
        else:
            coefficient = KEY_PRODUCT_COEFFICIENT
            print_('WARNING: Unexpected productLog on cartedOrPaidProductLogs:\n' + str(productLog))
        return coefficient * [sorted(viewedIstances, key = lambda instance: -instance[KEY_TIMESTAMP])[0]]
    return []
 
def extendLists(l):
    nl = []
    for e in l:
        nl.extend(e)
    return nl

def productInstances(logs):
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    searches = searches.map(idSetter)
    viewedProductLogs = viewedProductLogs.map(idSetter).collect()
    viewedProductIstances = extendLists([findViewedProductIstancesOnSearches(productLog, searches) for productLog in viewedProductLogs])
    print_high_logging(len(viewedProductIstances), 'product instances have been found from', 
                       len(viewedProductLogs), 'viewed productLogs on searches by', nowStr())
    #viewedProductIstances = sc_().parallelize(viewedProductIstances)
    cartedOrPaidIstances = cartedOrPaidProductLogs.map(idSetter) \
        .map(lambda productLog: findcartedOrPaidProductIstancesOnViews(productLog, viewedProductIstances)).reduce(lambda a, b: a+b)
    print_high_logging(len(cartedOrPaidIstances), 'carted or paid instances have been found from', 
                       len(cartedOrPaidProductLogs), 'carted or paid productLogs on searches by', nowStr())
    #return viewedProductIstances.union(sc_().parallelize(cartedOrPaidIstances))
    return sc_().parallelize(viewedProductIstances + cartedOrPaidIstances)

def pairsList(productLog):
    pList = []
    for otherId in productLog[KEY_PREFERRED_ID_LIST]:
        pList.append((productLog[KEY_ID], otherId))
        pList.append((otherId, productLog[KEY_ID]))
    return pList

def trainingInstancesForSingleKeyword(logs):
    instances = productInstances(logs)
    pairs = istances.map(pairsList).reduce(lambda a, b: a+b)
    print_logging(len(pairs), ' pairs have been found from', instances.count(), ' instances in total', nowStr())
    return pairs

c = 0
def trainingInstancesByKeywords(keywordDict):
    trainingInstancesDict = {}
    for keyword in keywordDict:
        global c
        c += 1
        print_logging(str(c)+'.', keyword.upper() + ':')
        trainingInstancesDict[keyword] = trainingInstancesForSingleKeyword(keywordDict[keyword])
    print_logging()
    return trainingInstancesDict