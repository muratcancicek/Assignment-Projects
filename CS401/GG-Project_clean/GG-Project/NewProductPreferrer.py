KEY_PREFERRED_ID_LIST ='preferred_ids'
KEY_PRODUCT_COEFFICIENT = 1
KEY_CART_COEFFICIENT = 10
KEY_PAYMENT_COEFFICIENT = 50
def specificPreviousSearchesWithId(productLog, search):
    import LumberjackConstants as L
    onSearch = False
    if isinstance(productLog[L.KEY_ID], int):
        if productLog[L.KEY_ID] in search[L.KEY_ID_LIST]:
            onSearch = True
    elif isinstance(productLog[L.KEY_ID], str):
        if '%7C' in productLog[L.KEY_ID]:
            processedIds = [int(i) for i in productLog[L.KEY_ID].split('%7C')]
            for id in processedIds:
                if id in search[L.KEY_ID_LIST]:
                    onSearch = True
                    break
    return onSearch

def instanceListFromActions(sp):
    import LumberjackConstants as L
    if sp[1][1][L.KEY_MODULE] == L.KEY_MODULE_CART:
        coefficient = KEY_CART_COEFFICIENT
    if sp[1][1][L.KEY_MODULE] == L.KEY_MODULE_PAYMENT:
        coefficient = KEY_PAYMENT_COEFFICIENT
    else:
        coefficient = KEY_PRODUCT_COEFFICIENT
    if isinstance(sp[1][1][L.KEY_ID], int):
        return coefficient * [(sp[1][1][L.KEY_ID], sp[0][L.KEY_ID_LIST][:sp[0][L.KEY_ID_LIST].index(sp[1][1][L.KEY_ID])])]
    else:
        processedIds = [int(i) for i in sp[1][1][L.KEY_ID].split('%7C')]
        s = []
        for pid in processedIds:
            if pid in sp[0][L.KEY_ID_LIST]:
                s.extend(coefficient * [(sp[1][1][L.KEY_ID], sp[0][L.KEY_ID_LIST][:sp[0][L.KEY_ID_LIST].index(pid)])])
        return s
a = False
def labelPairs(s):
    pairs = []
    for i in s[1]:
        pairs.append(((s[0], i), 1))
        pairs.append(((i, s[0]), 0))
    return pairs

def getLabeledPairs(searches, productLogs):
    import SparkLogFileHandler, LumberjackConstants as L
    searchedLogs = SparkLogFileHandler.sc_().parallelize([])
    for id_key in [L.KEY_PERSISTENT_COOKIE,L.KEY_USER_ID_FROM_COOKIE,L.KEY_USER_ID,L.KEY_SESSION_ID]:
        subSearches = searches.map(lambda search: (search[id_key], search))
        if productLogs.isEmpty():
            PythonVersionHandler.print_logging('0 pairs have been found by', nowStr())
        pair = productLogs.first()
        if isinstance(pair, tuple):  
            productLogs = productLogs.map(lambda kv: (kv[1][1][id_key], (kv[0], kv[1][1])))
        else:
            productLogs = productLogs.map(lambda kv: (kv[id_key], (kv[L.KEY_ID], kv)))
        subSearches = subSearches.join(productLogs)
        searchedLogs = searchedLogs.union(subSearches)
    searchedLogs = searchedLogs.map(lambda sp: sp[1]).filter(lambda sp: sp[0][L.KEY_TIMESTAMP] < sp[1][1][L.KEY_TIMESTAMP])
    searchedLogs = searchedLogs.filter(lambda sp: specificPreviousSearchesWithId(sp[1][1], sp[0]))
    searchedLogs = searchedLogs.map(lambda sp: str(sp)).distinct().map(lambda sp: eval(sp))
    searchedLogs = searchedLogs.sortBy(lambda sp: sp[1][1][L.KEY_TIMESTAMP], ascending = False)\
        .groupBy(lambda sp: sp[1][1][L.KEY_TIMESTAMP])\
        .map(lambda tsp: list(tsp[1])[0])
    pairs = searchedLogs.flatMap(lambda s: instanceListFromActions(s))
    pairs = pairs.flatMap(labelPairs)
    return pairs

def trainingInstancesForSingleKeyword(logs):
    import PythonVersionHandler, SparkLogFileHandler, Sessionizer
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    if searches.isEmpty() or (viewedProductLogs.isEmpty() and cartedOrPaidProductLogs.isEmpty()):
        PythonVersionHandler.print_logging('0 pairs have been found by', nowStr())
        return SparkLogFileHandler.sc_().parallelize([])
    searches = searches.map(Sessionizer.idSetter)
    viewedProductLogs = viewedProductLogs.map(lambda kv: Sessionizer.idSetter(kv[1]))
    cartedOrPaidProductLogs = cartedOrPaidProductLogs.map(lambda kv: Sessionizer.idSetter(kv[1][1]))
    pairs = getLabeledPairs(searches, viewedProductLogs.union(cartedOrPaidProductLogs))
    if pairs.count() > 0:
        PythonVersionHandler.print_logging(pairs.count(), 'pairs have been found by', nowStr())
    else:
        PythonVersionHandler.print_logging('0 pairs have been found by', nowStr())
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
        PythonVersionHandler.print_logging(trainingInstancesDict[keyword].count(), 'pairs have been labeled by', PythonVersionHandler.nowStr())
        PythonVersionHandler.print_logging()
    return trainingInstancesDict
