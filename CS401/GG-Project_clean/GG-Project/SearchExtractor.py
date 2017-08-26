
#from urllib.parse import urlparse

def iriTest():
    print_(refererParser('http%3A%2F%2Fwww.gittigidiyor.com%2Farama%2F%3Fk%3Dnike%2520%25C3%25A7ocuk%2520ayakkab%25C4%25B1'))

def isProduct(log):
    import LumberjackConstants as L
    return (log[L.KEY_MODULE] in [L.KEY_MODULE_ITEM, L.KEY_MODULE_CART, L.KEY_MODULE_PAYMENT]) if L.KEY_MODULE in log.keys() else False

def isSearch(log):
    import LumberjackConstants as L
    return (log[L.KEY_MODULE] == L.KEY_MODULE_SEARCH and L.KEY_KEYWORD in log.keys()) if L.KEY_MODULE in log.keys() else False

def specificSearches(logs, keywords):
    import LumberjackConstants as L
    searches = logs.filter(isSearch)
    if len(keywords) == 1: 
        keyword = keywords[0]; 
        return searches.filter(lambda log: L.KEY_ID_LIST in log.keys() and str(log[L.KEY_KEYWORD]).lower() == keyword)
    else:
        return searches.filter(lambda log: L.KEY_ID_LIST in log.keys() and str(log[L.KEY_KEYWORD]).lower() in keywords)

def findExistingSearchKeywords(filteredPath):
    import LumberjackConstants as L
    logs = getLogs(None, filteredPath, False)
    logs = logs.filter(lambda log: log[L.KEY_MODULE] == L.KEY_MODULE_SEARCH and L.KEY_KEYWORD in log.keys())
    keywords32 = get32Keywords()
    logs = logs.filter(lambda log: str([L.KEY_KEYWORD]).lower() in keywords32)
    logs = logs.map(lambda log: log[L.KEY_KEYWORD])
    keywords = logs.distinct()
    print(keywords.count(), 'keywords has been found in data by', PythonVersionHandler.nowStr())
    return keywords.collect()

def refererParser(rawReferer):
    if isinstance(rawReferer, dict): return rawReferer
    import urllib, StringUtil , LumberjackConstants as L
    rawReferer = StringUtil.convertTrChars(urllib.parse.unquote_plus(urllib.parse.unquote_plus(rawReferer)))
    scheme, authority, path, params, query, frag = urllib.parse.urlparse(rawReferer) 
    query = [p.split('=') for p in query.split('&')]
    query = [p for p in query if len(p) == 2]
    referer = {p[0]: p[1] for p in query}
    referer['page'] = path[1:]
    return referer 

def refererParserOnLog(log):
    import LumberjackConstants as L
    if L.KEY_REFERER in log.keys():
        log[L.KEY_REFERER] = refererParser(log[L.KEY_REFERER])
    else:
        log[L.KEY_REFERER] = {}
    return log
 
def specificProductLogs(logs, keywords):
    import LumberjackConstants as L
    def isProductLogsFromSearchOrItems(log):
        import LumberjackConstants as L
        if isProduct(log):
            referer = refererParserOnLog(log)[L.KEY_REFERER] 
            referer = refererParser(log[L.KEY_REFERER]) if type(log[L.KEY_REFERER]) == str else log[L.KEY_REFERER]
            if log[L.KEY_MODULE] == L.KEY_MODULE_ITEM:
                if 'page' in referer.keys() and referer['page'] == 'arama/' and 'k' in referer.keys():
                    return referer['k'] in keywords
                else:
                    return False
            elif log[L.KEY_MODULE] == L.KEY_MODULE_CART:
                return 'page' in referer.keys() and str(log[L.KEY_ID]) in referer['page']
            elif log[L.KEY_MODULE] == L.KEY_MODULE_PAYMENT:
                return True
        else:
            False
    return logs.filter(isProductLogsFromSearchOrItems)

def productLogsFromBySingleKeyword(searches, productLogs, keyword):
    import SparkLogReader, LumberjackConstants as L
    listedIds = searches.flatMap(lambda log: log[L.KEY_ID_LIST]).distinct().map(lambda i: (i, i))
    import PythonVersionHandler
    PythonVersionHandler.print_high_logging(listedIds.count(), 'products have listed on searches for', keyword, 'by', PythonVersionHandler.nowStr())
    viewedProductLogs = productLogs.filter(lambda log: log[L.KEY_MODULE] == L.KEY_MODULE_ITEM and log[L.KEY_REFERER]['k'] == keyword)
    PythonVersionHandler.print_high_logging(viewedProductLogs.count(), 'views have found for', keyword, 'by', PythonVersionHandler.nowStr())
    viewedProductLogs = viewedProductLogs.map(lambda log: (log[L.KEY_ID], log))
    viewedProductLogs = listedIds.join(viewedProductLogs)
    viewedIds = viewedProductLogs.map(lambda kv: (kv[0], kv[0])).distinct()
    viewedProductLogs = viewedProductLogs.map(lambda kv: kv[1][1])
    PythonVersionHandler.print_logging(viewedIds.count(), 'products have clicked on searches for', keyword, 'by', PythonVersionHandler.nowStr())
    cartedOrPaidProductLogs = productLogs.filter(lambda log: log[L.KEY_MODULE] == L.KEY_MODULE_CART or log[L.KEY_MODULE] == L.KEY_MODULE_PAYMENT)
    def singleId(log):
        try:
            import LumberjackConstants as L
            if isinstance(log[L.KEY_ID], int):
                return [(log[L.KEY_ID], log)]
            if isinstance(log[L.KEY_ID], str):
                if '%7C' in log[L.KEY_ID]:
                    return [(int(i), log) for i in log[L.KEY_ID].split('%7C')]
        except TypeError:
            print(log[L.KEY_ID], 'not iteratable at SearchExtractor line 96')
            raise TypeError
    cartedOrPaidProductLogs = viewedIds.join(cartedOrPaidProductLogs.flatMap(singleId)).map(lambda kv: kv[1][1])
    PythonVersionHandler.print_logging(cartedOrPaidProductLogs.count(), 'cart and payments have found for', keyword, 'by', PythonVersionHandler.nowStr())
    return viewedProductLogs, cartedOrPaidProductLogs

def untuple(log):
    if isinstance(log, tuple): 
        if isinstance(log[1], tuple): return log[1][1]
        else: return log[1]
    else: return log

def searchNProductLogsBySingleKeyword(searches, productLogs, keyword):
    import LumberjackConstants as L
    import PythonVersionHandler, SparkLogFileHandler
    searches = searches.filter(lambda log: log[L.KEY_KEYWORD] == keyword)
    PythonVersionHandler.print_logging(searches.count(), 'searches have found for', keyword, 'by', PythonVersionHandler.nowStr())
    if searches.count() == 0:
        PythonVersionHandler.print_logging()
        return (searches, SparkLogFileHandler.sc_().parallelize([]), SparkLogFileHandler.sc_().parallelize([]))
    viewedProductLogs, cartedOrPaidProductLogs = productLogsFromBySingleKeyword(searches, productLogs, keyword)
    if not PythonVersionHandler.LOGGING: PythonVersionHandler.print_(searches.count(), 'searches,', viewedProductLogs.count(), 'views,', cartedOrPaidProductLogs.count(), 
           'cart and payments have found for', keyword, 'by', PythonVersionHandler.nowStr())
    #PythonVersionHandler.print_logging()
    return (searches, viewedProductLogs.map(untuple), cartedOrPaidProductLogs.map(untuple))

def searchNProductLogsForSingleKeyword(logs, keywords, parsed = False):
    if parsed:
        logs = logs.map(untuple)
    import PythonVersionHandler
    if isinstance(keywords, str): 
        keywords = [keywords]
    searches = specificSearches(logs, keywords)
    productLogs = specificProductLogs(logs, keywords)
    return searchNProductLogsBySingleKeyword(searches, productLogs, keywords[0])

def searchNProductLogsByKeywords(logs, keywords, parsed = False):
    if parsed:
        logs = logs.map(untuple)
    import PythonVersionHandler
    if isinstance(keywords, str): 
        keywords = [keywords]
    searches = specificSearches(logs, keywords)
    PythonVersionHandler.print_logging(searches.count(), 'searches have found relevant with', len(keywords), 'keywords by', PythonVersionHandler.nowStr())
    productLogs = specificProductLogs(logs, keywords)
    PythonVersionHandler.print_logging(productLogs.count(), 'productLogs have found relevant with', len(keywords), 'keywords by', PythonVersionHandler.nowStr(), '\n')
    d = {keyword: searchNProductLogsBySingleKeyword(searches, productLogs, keyword) for keyword in keywords}
    global c
    return d