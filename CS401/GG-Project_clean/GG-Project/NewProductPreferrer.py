from paths import *
from PythonVersionHandler import *
from SearchExtractor import *
from LumberjackConstants import *
from Sessionizer import *

KEY_PREFERRED_ID_LIST ='preferred_ids'
KEY_PRODUCT_COEFFICIENT = 1
KEY_CART_COEFFICIENT = 10
KEY_PAYMENT_COEFFICIENT = 50
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

def instanceListFromActions(sp):
    if sp[1][1][KEY_MODULE] == KEY_MODULE_CART:
        coefficient = KEY_CART_COEFFICIENT
    if sp[1][1][KEY_MODULE] == KEY_MODULE_PAYMENT:
        coefficient = KEY_PAYMENT_COEFFICIENT
    else:
        coefficient = KEY_PRODUCT_COEFFICIENT
    if isinstance(sp[1][1][KEY_ID], int):
        return coefficient * [(sp[1][1][KEY_ID], sp[0][KEY_ID_LIST][:sp[0][KEY_ID_LIST].index(sp[1][1][KEY_ID])])]
    else:
        processedIds = [int(i) for i in productLog[KEY_ID].split('%7C')]
        s = []
        for pid in processedIds:
            if pid in sp[0][KEY_ID_LIST]:
                s.extend(coefficient * [(sp[1][KEY_ID], sp[0][KEY_ID_LIST][:sp[0][KEY_ID_LIST].index(pid)])])
        return s
a = False
def labelPairs(s):
    s = []
    global a
    if not a:
        print_(s)
        a = True
    for i in s[1]:
        s.append(((s[0], i), 1))
        s.append(((i, s[0]), 0))
    return s

def getLabeledPairs(searches, productLogs):
    import SparkLogFileHandler
    searchedLogs = SparkLogFileHandler.sc_().parallelize([])
    for id_key in [KEY_PERSISTENT_COOKIE,KEY_USER_ID_FROM_COOKIE,KEY_USER_ID,KEY_SESSION_ID]:
        subSearches = searches.map(lambda search: (search[id_key], search))
        pair = productLogs.first()
        if isinstance(pair, tuple):  
            productLogs = productLogs.map(lambda kv: (kv[1][1][id_key], (kv[0], kv[1][1])))
        else:
            productLogs = productLogs.map(lambda kv: (kv[id_key], (kv[KEY_ID], kv)))
        subSearches = subSearches.join(productLogs)
        searchedLogs = searchedLogs.union(subSearches)
    searchedLogs = searchedLogs.map(lambda sp: sp[1]).filter(lambda sp: sp[0][KEY_TIMESTAMP] < sp[1][1][KEY_TIMESTAMP])
    searchedLogs = searchedLogs.filter(lambda sp: specificPreviousSearchesWithId(sp[1][1], sp[0]))
    searchedLogs = searchedLogs.map(lambda sp: str(sp)).distinct().map(lambda sp: eval(sp))
    searchedLogs = searchedLogs.sortBy(lambda sp: sp[1][1][KEY_TIMESTAMP], ascending = False)\
        .groupBy(lambda sp: sp[1][1][KEY_TIMESTAMP])\
        .map(lambda tsp: list(tsp[1])[0])
    print_(searchedLogs.count(), "logs", nowStr())
    pairs = searchedLogs.flatMap(lambda s: instanceListFromActions(s))
    print_(pairs.count(), "pair", nowStr())
    pairs = pairs.flatMap(labelPairs)
    print_(pairs.count(), "pair", nowStr())
    return pairs

def trainingInstancesForSingleKeyword(logs):
    import PythonVersionHandler
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    searches = searches.map(idSetter)
    viewedProductLogs = viewedProductLogs.map(lambda kv: idSetter(kv[1]))
    cartedOrPaidProductLogs = cartedOrPaidProductLogs.map(lambda kv: idSetter(kv[1][1]))
    pairs = getLabeledPairs(searches, viewedProductLogs.union(cartedOrPaidProductLogs))
    if pairs.count() > 0:
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