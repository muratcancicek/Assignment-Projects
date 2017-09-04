KEY_PREFERRED_ID_LIST ='preferred_ids'
KEY_PRODUCT_COEFFICIENT = 1
KEY_CART_COEFFICIENT = 10
KEY_PAYMENT_COEFFICIENT = 50

def isProductIdOnSearch(productLog, search):
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

def pairSearchesNProducts(searches, productLogs):
    import PythonVersionHandler, SparkLogFileHandler, LumberjackConstants as L
    searchesNProducts = SparkLogFileHandler.sc_().parallelize([])
    for id_key in [L.KEY_PERSISTENT_COOKIE,L.KEY_USER_ID_FROM_COOKIE,L.KEY_USER_ID,L.KEY_SESSION_ID]:
        subSearches = searches.map(lambda search: (search[id_key], search))
        if productLogs.isEmpty():
            PythonVersionHandler.print_logging('0 pairs have been found by', PythonVersionHandler.nowStr())
            return searchesNProducts
        pair = productLogs.first()
        if isinstance(pair, tuple):  
            productLogs = productLogs.map(lambda kv: (kv[1][1][id_key], (kv[0], kv[1][1])))
        else:
            productLogs = productLogs.map(lambda kv: (kv[id_key], (kv[L.KEY_ID], kv)))
        subSearches = subSearches.join(productLogs)
        searchesNProducts = searchesNProducts.union(subSearches)
    searchesNProducts = searchesNProducts.map(lambda sp: sp[1]).filter(lambda sp: sp[0][L.KEY_TIMESTAMP] < sp[1][1][L.KEY_TIMESTAMP])
    searchesNProducts = searchesNProducts.map(lambda sp: str(sp)).distinct().map(lambda sp: eval(sp))
    return searchesNProducts

def instanceListFromActions(sp, productOnPage = True):
    import LumberjackConstants as L
    if sp[1][1][L.KEY_MODULE] == L.KEY_MODULE_CART:
        coefficient = KEY_CART_COEFFICIENT
    elif sp[1][1][L.KEY_MODULE] == L.KEY_MODULE_PAYMENT:
        coefficient = KEY_PAYMENT_COEFFICIENT
    else:
        coefficient = KEY_PRODUCT_COEFFICIENT
    if isinstance(sp[1][1][L.KEY_ID], int):
        l = sp[0][L.KEY_ID_LIST][:sp[0][L.KEY_ID_LIST].index(sp[1][1][L.KEY_ID])] if productOnPage else sp[0][L.KEY_ID_LIST]
        return coefficient * [(sp[1][1][L.KEY_ID], l)]
    else:
        processedIds = [int(i) for i in sp[1][1][L.KEY_ID].split('%7C')]
        s = []
        for pid in processedIds:
            if pid in sp[0][L.KEY_ID_LIST]:
                l = sp[0][L.KEY_ID_LIST][:sp[0][L.KEY_ID_LIST].index(pid)] if productOnPage else sp[0][L.KEY_ID_LIST]
                s.extend(coefficient * [(pid, l)])
        return s

def instanceListFromPrevious(sp):
    return instanceListFromActions(sp, productOnPage = False)

def labelPairs(s):
    pairs = []
    for i in s[1]:
        pairs.append(((s[0], i), 1))
        pairs.append(((i, s[0]), 0))
    return pairs

def getLabeledPairsOnSinglePage(searchesNProducts):
    import LumberjackConstants as L
    searchesNProducts = searchesNProducts.filter(lambda sp: isProductIdOnSearch(sp[1][1], sp[0]))
    searchesNProducts = searchesNProducts.map(lambda sp: (sp[1][1][L.KEY_TIMESTAMP], sp))
    searchesNProducts = searchesNProducts.reduceByKey(lambda x1, x2: max(x1, x2, key=lambda x: x[0][L.KEY_TIMESTAMP])).map(lambda sp: sp[1])
    pairs = searchesNProducts.flatMap(instanceListFromActions)
    pairs = pairs.flatMap(labelPairs)
    return pairs, searchesNProducts

def pairSearchesNPrevious(searchesNProducts, pairedSearchesNProducts):
    import LumberjackConstants as L, PythonVersionHandler, SparkLogFileHandler
    endingSearches = pairedSearchesNProducts.filter(lambda sp: sp[0][L.KEY_PAGENUM] > 1)
    searchesNPrevious = SparkLogFileHandler.sc_().parallelize([])
    for id_key in [L.KEY_PERSISTENT_COOKIE,L.KEY_USER_ID_FROM_COOKIE,L.KEY_USER_ID,L.KEY_SESSION_ID]:
        subSearches = endingSearches.map(lambda kv: (kv[0][id_key], kv))
        previousSearches = searchesNProducts.map(lambda sp: (sp[0][id_key], sp))
        subSearches = subSearches.join(previousSearches)
        searchesNPrevious = searchesNPrevious.union(subSearches)
    searchesNPrevious = searchesNPrevious.map(lambda sp: sp[1]).map(lambda sp: str(sp)).distinct().map(lambda sp: eval(sp))
    searchesNPrevious = searchesNPrevious.filter(lambda sp: sp[0][1][1][L.KEY_ID] == sp[1][1][1][L.KEY_ID])
    return searchesNPrevious

def isSearchPrevious(sp):
    return sp[0][0][L.KEY_TIMESTAMP] > sp[1][0][L.KEY_TIMESTAMP] and sp[0][0][L.KEY_PAGENUM] > sp[1][0][L.KEY_PAGENUM]\
           and not isProductIdOnSearch(sp[0][1][1], sp[1][0])

def getLabeledPairsOnPreviousPages(searchesNProducts, pairedSearchesNProducts):
    searchesNPrevious = pairSearchesNPrevious(searchesNProducts, pairedSearchesNProducts)
    searchesNPrevious = searchesNPrevious.filter(isSearchPrevious) 
    searchesNPrevious = searchesNPrevious.map(lambda sp: (sp[1][0], sp[0][1][1]))
    pairs = searchesNPrevious.flatMap(instanceListFromPrevious)
    pairs = pairs.flatMap(labelPairs)
    return pairs

def getLabeledPairs(searches, productLogs):
    searchesNProducts = pairSearchesNProducts(searches, productLogs)
    pairs1, pairedSearchesNProducts = getLabeledPairsOnSinglePage(searchesNProducts)
    pairs2 = getLabeledPairsOnPreviousPages(searchesNProducts, pairedSearchesNProducts)
    return pairs1.union(pairs2)#

def trainingInstancesForSingleKeyword(logs):
    import PythonVersionHandler, SparkLogFileHandler, Sessionizer
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    if searches.isEmpty() or (viewedProductLogs.isEmpty() and cartedOrPaidProductLogs.isEmpty()):
        PythonVersionHandler.print_logging('0 pairs have been found by', PythonVersionHandler.nowStr())
        return SparkLogFileHandler.sc_().parallelize([])
    searches = searches.map(Sessionizer.idSetter)
    productLogs = viewedProductLogs.union(cartedOrPaidProductLogs).map(Sessionizer.idSetter)
    pairs = getLabeledPairs(searches, productLogs)
    if pairs.count() > 0:
        PythonVersionHandler.print_logging(pairs.count(), 'pairs have been found by', PythonVersionHandler.nowStr())
    else:
        PythonVersionHandler.print_logging('0 pairs have been found by', PythonVersionHandler.nowStr())
    return pairs

c = 0
def trainingInstancesByKeywords(keywordDict):
    trainingInstancesDict = {}
    import PythonVersionHandler
    global c
    for keyword in keywordDict:
        c += 1
        PythonVersionHandler.print_logging(str(c)+'.', keyword.upper() + ':')
        trainingInstancesDict[keyword] = trainingInstancesForSingleKeyword(keywordDict[keyword])
        PythonVersionHandler.print_logging(trainingInstancesDict[keyword].count(), 'pairs have been labeled by', PythonVersionHandler.nowStr())
        PythonVersionHandler.print_logging()
    c = 0
    return trainingInstancesDict
