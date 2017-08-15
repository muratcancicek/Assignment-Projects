from paths import *
from PythonVersionHandler import *
from SearchExtractor import *
from LumberjackConstants import *
from Sessionizer import *

KEY_PREFERRED_ID_LIST ='preferred_ids'
KEY_PRODUCT_COEFFICIENT = 1
KEY_CART_COEFFICIENT = 10
KEY_PAYMENT_COEFFICIENT = 50

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
    searches = searches.sortBy(lambda search: search[KEY_TIMESTAMP], ascending = False)
    if searches.count() > 0:
        search = searches.first()
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

def getLabeledPairs(searches, productLogs):
    import SparkLogFileHandler
    searchedLogs = SparkLogFileHandler.sc_().parallelize([])
    for id_key in [KEY_PERSISTENT_COOKIE,KEY_USER_ID_FROM_COOKIE,KEY_USER_ID,KEY_SESSION_ID]:
        searches = searches.map(lambda search: (search[id_key], search))
        pair = productLogs.first()
        if isinstance(pair, tuple):  
            productLogs = productLogs.map(lambda kv: (kv[1][1][id_key], (kv[0], kv[1][1])))
        else:
            productLogs = productLogs.map(lambda kv: (kv[id_key], (kv[KEY_ID], kv)))
        searchedLogs.join(searches.join(productLogs))
    searchedLogs = searchedLogs.distinct()
    searchedLogs = searchedLogs.map(lambda sp: sp[0][KEY_TIMESTAMP] < sp[1][KEY_TIMESTAMP] and specificPreviousSearchesWithId(sp[1], sp[0]))
    searchedLogs = searchedLogs.sortBy(lambda sp: sp[1][KEY_TIMESTAMP], ascending = False)\
        .groupBy(lambda sp: sp[1][KEY_TIMESTAMP])\
        .map(lambda tsp: tsp[1][0])
    def idPairs(sp):
        if sp[1][KEY_MODULE] == KEY_MODULE_CART:
            coefficient = KEY_CART_COEFFICIENT
        if sp[1][KEY_MODULE] == KEY_MODULE_PAYMENT:
            coefficient = KEY_PAYMENT_COEFFICIENT
        else:
            coefficient = KEY_PRODUCT_COEFFICIENT
        if isInstance(sp[1][KEY_ID], int):
            return coefficient * [(sp[1][KEY_ID], sp[0][KEY_ID_LIST][:sp[0][KEY_ID_LIST].index(sp[1][KEY_ID])])]
        else:
            processedIds = [int(i) for i in productLog[KEY_ID].split('%7C')]
            s = []
            for pid in processedIds:
                if pid in sp[0][KEY_ID_LIST]:
                   s.extend(coefficient * [(sp[1][KEY_ID], sp[0][KEY_ID_LIST][:sp[0][KEY_ID_LIST].index(pid)])])
            return s
    def pairn(s):
        s = []
        for i in s[1]:
            s.append(((s[0], i), 1))
            s.append(((i, s[0]), 0))
        return s
    pairs = searchedLogs.map(idPairs).flatMap(lambda s: s).flatMap(pairn)
    return pairs

def productInstances(logs):
    import PythonVersionHandler
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    searches = searches.map(idSetter)
    viewedProductLogs = viewedProductLogs.map(lambda kv: idSetter(kv[1])).collect()
    viewedProductIstances = extendLists([findViewedProductIstancesOnSearches(productLog, searches) for productLog in viewedProductLogs])
    PythonVersionHandler.print_high_logging(len(viewedProductIstances), 'product instances have been found from', 
                       len(viewedProductLogs), 'viewed productLogs on searches by', PythonVersionHandler.nowStr())
    #viewedProductIstances = sc_().parallelize(viewedProductIstances)
    cartedOrPaidIstances = cartedOrPaidProductLogs.map(lambda kv: idSetter(kv[1][1])) \
        .map(lambda productLog: findcartedOrPaidProductIstancesOnViews(productLog, viewedProductIstances))
    if cartedOrPaidIstances.count() > 0:
        cartedOrPaidIstances = cartedOrPaidIstances.reduce(lambda a, b: a+b)
        PythonVersionHandler.print_high_logging(len(cartedOrPaidIstances), 'carted or paid instances have been found from', 
                           cartedOrPaidProductLogs.count(), 'carted or paid productLogs on searches by', PythonVersionHandler.nowStr())
    else:
        cartedOrPaidIstances = []
        PythonVersionHandler.print_high_logging(len(cartedOrPaidIstances), 'carted or paid instances have been found from', 
                           cartedOrPaidProductLogs.count(), 'carted or paid productLogs on searches by', PythonVersionHandler.nowStr())

    #return viewedProductIstances.union(sc_().parallelize(cartedOrPaidIstances))
    return sc_().parallelize(viewedProductIstances + cartedOrPaidIstances)

def pairsList(productLog):
    pList = []
    for otherId in productLog[KEY_PREFERRED_ID_LIST]:
        pList.append((productLog[KEY_ID], otherId))
        pList.append((otherId, productLog[KEY_ID]))
    return pList

def trainingInstancesForSingleKeyword(logs):
    import PythonVersionHandler
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    searches = searches.map(idSetter)
    viewedProductLogs = viewedProductLogs.map(lambda kv: idSetter(kv[1]))
    cartedOrPaidProductLogs = cartedOrPaidProductLogs.map(lambda kv: idSetter(kv[1][1]))
    pairs = getLabeledPairs(searches, viewedProductLogs.union(cartedOrPaidProductLogs))
    if pairs.count() > 0:
        pairs = pairs.reduce(lambda a, b: a+b)
        PythonVersionHandler.print_logging(pairs.count(), 'pairs have been found in total', nowStr())
    else:
        PythonVersionHandler.print_logging('0 pairs have been found from in total', nowStr())
    return pairs

c = 0
def trainingInstancesByKeywords(keywordDict):
    trainingInstancesDict = {}
    import PythonVersionHandler
    for keyword in keywordDict:
        global c
        c += 1
        PythonVersionHandler.print_logging(str(c)+'.', keyword.upper() + ':')
        trainingInstancesDict[keyword] = trainingInstancesForSingleKeyword(keywordDict[keyword])
    PythonVersionHandler.print_logging()
    return trainingInstancesDict