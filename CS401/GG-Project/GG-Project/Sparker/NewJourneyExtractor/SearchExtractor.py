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
    if isinstance(keywords, str): 
        keyword = keywords; return searches.filter(lambda log: log[KEY_KEYWORD].lower() == keyword)
    else:
        return searches.filter(lambda log: log[KEY_KEYWORD].lower() in keywords)

def findExistingSearchKeywords(filteredPath):
    logs = getLogs(None, filteredPath, False)
    logs = logs.filter(lambda log: log[KEY_MODULE] == KEY_MODULE_SEARCH and KEY_KEYWORD in log.keys())
    keywords32 = get32Keywords()
    logs = logs.filter(lambda log: log[KEY_KEYWORD].lower() in keywords32)
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

def refersFromSearch(log):
    referer = log[KEY_REFERER] 
    referer = refererParser(log[KEY_REFERER]) if type(log[KEY_REFERER]) == str else log[KEY_REFERER]
    return 'page' in referer.keys() and referer['page'] == 'arama/' and 'k' in referer.keys()

#def idsFromSearches(searches):
#    fourIds = lambda log: (log[KEY_PERSISTENT_COOKIE], log[KEY_USER_ID_FROM_COOKIE], log[KEY_USER_ID], log[KEY_SESSION_ID])
#    idTuplus = searches.map(fourIds).collect()
#    ids = set()
#    for tple in idTuplus:
#        ids.union(tple)
#    return ids

#def productLogsBySearchCookies(logs, searches):
#    ids = idsFromSearches(searches)
#    return logs.filter(lambda log: isProduct(log) and log[KEY_PERSISTENT_COOKIE] in cookies)
 
def productLogsBySearchReferers(logs, searches):
    #productLogs = productLogsBySearchCookies(logs, searches)
    productLogs = logs.filter(lambda log: isProduct(log))
    return productLogs.map(refererParserOnLog).filter(refersFromSearch)

def searchNProductLogsBySingleKeyword(searches, productLogs, keyword):
    searches = searches.filter(lambda log: log[KEY_KEYWORD] == keyword)
    productLogs = productLogs.filter(lambda log: log[KEY_REFERER]['k'] == keyword)
    return (searches, productLogs)

def searchNProductLogsByKeywords(logs, keywords):
    searches = specificSearches(logs, keywords)
    productLogs = productLogsBySearchReferers(logs, searches)
    if isinstance(keywords, str): 
        keyword = keywords; return {keyword: searchNProductLogsBySingleKeyword(searches, productLogs, keyword)}
    else:
        return {keyword: searchNProductLogsBySingleKeyword(searches, productLogs, keyword) for keyword in keywords}
