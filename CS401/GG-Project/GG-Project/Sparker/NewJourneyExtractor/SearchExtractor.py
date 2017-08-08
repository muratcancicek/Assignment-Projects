from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from LogProcesser.scalaToPython.python_codes.StringUtil import *
from Sparker.NewJourneyExtractor.BotFilter import *
from urllib.parse import urlparse
import urllib

def iriTest():
    print_(refererParser('http%3A%2F%2Fwww.gittigidiyor.com%2Farama%2F%3Fk%3Dnike%2520%25C3%25A7ocuk%2520ayakkab%25C4%25B1'))

def isProduct(log):
    return log[KEY_MODULE] in [KEY_MODULE_ITEM, KEY_MODULE_CART, KEY_MODULE_PAYMENT]

def isSearch(log):
    return log[KEY_MODULE] == KEY_MODULE_SEARCH and KEY_KEYWORD in log.keys()

def specificSearches(logs, keywords):
    searches = logs.filter(isSearch)
    if len(keywords) == 1: 
        keyword = keywords[0]; return searches.filter(lambda log: KEY_ID_LIST in log.keys() and str(log[KEY_KEYWORD]).lower() == keyword)
    else:
        return searches.filter(lambda log: KEY_ID_LIST in log.keys() and str(log[KEY_KEYWORD]).lower() in keywords)

def findExistingSearchKeywords(filteredPath):
    logs = getLogs(None, filteredPath, False)
    logs = logs.filter(lambda log: log[KEY_MODULE] == KEY_MODULE_SEARCH and KEY_KEYWORD in log.keys())
    keywords32 = get32Keywords()
    logs = logs.filter(lambda log: str([KEY_KEYWORD]).lower() in keywords32)
    logs = logs.map(lambda log: log[KEY_KEYWORD])
    keywords = logs.distinct()
    print(keywords.count(), 'keywords has been found in data by', nowStr())
    return keywords.collect()

def refererParser(rawReferer):
    rawReferer = convertTrChars(urllib.parse.unquote_plus(urllib.parse.unquote_plus(rawReferer)))
    scheme, authority, path, params, query, frag = urlparse(rawReferer) 
    query = [p.split('=') for p in query.split('&')]
    query = [p for p in query if len(p) == 2]
    referer = {p[0]: p[1] for p in query}
    referer['page'] = path[1:]
    return referer 

def refererParserOnLog(log):
    if KEY_REFERER in log.keys():
        log[KEY_REFERER] = refererParser(log[KEY_REFERER])
    else:
        log[KEY_REFERER] = {}
    return log
 
def specificProductLogs(logs, keywords):
    def isProductLogsFromSearchOrItems(log):
        if isProduct(log):
            referer = refererParserOnLog(log)[KEY_REFERER] 
            referer = refererParser(log[KEY_REFERER]) if type(log[KEY_REFERER]) == str else log[KEY_REFERER]
            if log[KEY_MODULE] == KEY_MODULE_ITEM:
                if 'page' in referer.keys() and referer['page'] == 'arama/' and 'k' in referer.keys():
                    return referer['k'] in keywords
                else:
                    return False
            elif log[KEY_MODULE] == KEY_MODULE_CART:
                return 'page' in referer.keys() and str(log[KEY_ID]) in referer['page']
            elif log[KEY_MODULE] == KEY_MODULE_PAYMENT:
                return True
        else:
            False
    return logs.filter(isProductLogsFromSearchOrItems)

def productLogsFromBySingleKeyword(searches, productLogs, keyword):
    listedIds = uniqueList(searches.map(lambda log: log[KEY_ID_LIST]).reduce(lambda a, b: a+b))
    print_high_logging(len(listedIds), 'products have listed on searches for', keyword, 'by', nowStr())
    viewedProductLogs = productLogs.filter(lambda log: log[KEY_ID] in listedIds \
        and log[KEY_MODULE] == KEY_MODULE_ITEM and log[KEY_REFERER]['k'] == keyword)
    print_high_logging(viewedProductLogs.count(), 'views have found for', keyword, 'by', nowStr())
    viewedIds = viewedProductLogs.map(lambda log: log[KEY_ID]).distinct().collect()
    print_logging(len(viewedIds), 'products have clicked on searches for', keyword, 'by', nowStr())
    cartedOrPaidProductLogs = productLogs.filter(lambda log: log[KEY_MODULE] == KEY_MODULE_CART \
        or log[KEY_MODULE] == KEY_MODULE_PAYMENT)
    def isViewed(log):
        if isinstance(log[KEY_ID], int):
            return log[KEY_ID] in viewedIds 
        if isinstance(log[KEY_ID], str):
            if '%7C' in log[KEY_ID]:
                #print(log[KEY_ID])
                processedIds = [int(i) for i in log[KEY_ID].split('%7C')]
                for i in processedIds:
                    if i in viewedIds:
                        return True
            return log[KEY_ID] in viewedIds 
    cartedOrPaidProductLogs = cartedOrPaidProductLogs.filter(isViewed)
    print_logging(cartedOrPaidProductLogs.count(), 'cart and payments have found for', keyword, 'by', nowStr())
    return viewedProductLogs, cartedOrPaidProductLogs

c = 0
def searchNProductLogsBySingleKeyword(searches, productLogs, keyword):
    global c
    c += 1
    print_logging(str(c)+'.', keyword.upper() + ':')
    searches = searches.filter(lambda log: log[KEY_KEYWORD] == keyword)
    print_logging(searches.count(), 'searches have found for', keyword, 'by', nowStr())
    if searches.count() == 0:
        print_logging()
        return (searches, sc_().parallelize([]), sc_().parallelize([]))
    viewedProductLogs, cartedOrPaidProductLogs = productLogsFromBySingleKeyword(searches, productLogs, keyword)
    if not LOGGING: print_(searches.count(), 'searches,', viewedProductLogs.count(), 'views,', cartedOrPaidProductLogs.count(), 
           'cart and payments have found for', keyword, 'by', nowStr())
    print_logging()
    return (searches, viewedProductLogs, cartedOrPaidProductLogs)

def searchNProductLogsByKeywords(logs, keywords):
    if isinstance(keywords, str): 
        keywords = [keywords]
    searches = specificSearches(logs, keywords)
    print_logging(searches.count(), 'searches have found relevant with', len(keywords), 'keywords by', nowStr())
    productLogs = specificProductLogs(logs, keywords)
    print_logging(productLogs.count(), 'productLogs have found relevant with', len(keywords), 'keywords by', nowStr(), '\n')
    return {keyword: searchNProductLogsBySingleKeyword(searches, productLogs, keyword) for keyword in keywords}
