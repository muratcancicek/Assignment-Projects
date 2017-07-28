from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from LogProcesser.scalaToPython.python_codes.StringUtil import *
from Sparker.NewJourneyExtractor.BotFilter import *
from urllib.parse import urlparse
import urllib

def filteringTest():
    #fromPath = joinPath(may17Folder, '2017-05-16/part-r-00000')
    fromPath = 'hdfs://osldevptst02.host.gittigidiyor.net:8020/user/root/searchlogs/2017-05-16/part-r-00000.gz'
    #fromPath = joinPath(clickstreamFolder, 'part-r-00000')
    toPath = joinPath(clickstreamFolder, 'part-r-00000_filtered')
    filterSaveLogs(fromPath, toPath)
    

def get32Keywords():
    keywords = open(joinPath(rankingFolder, 'keywords'), 'rb').readlines()
    keywords = [convertTrChars(keyword.decode("utf-8")).replace('\n', '').lower() for keyword in keywords]
    return keywords

def get5Keywords():
    return ['lg g4', 'samsung galaxy s6', 'galaxy s3', 'nike air max', 'tupperware']

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
    log[KEY_REFERER] = refererParser(log[KEY_REFERER])
    return log

def refersFromSearch(log):
    referer = log[KEY_REFERER] if KEY_REFERER in log.keys() else {}
    referer = refererParser(log[KEY_REFERER]) if type(log[KEY_REFERER]) == str else log[KEY_REFERER]
    return 'page' in referer.keys() and referer['page'] == 'arama/' and 'k' in referer.keys()

def productLogsBySearchCookies(logs, searches):
    cookies = searches.map(lambda log: log[KEY_PERSISTENT_COOKIE]).distinct().collect()
    return logs.filter(lambda log: isProduct(log) and log[KEY_PERSISTENT_COOKIE] in cookies)
 
def productLogsBySearchReferers(logs, searches):
    productLogs = productLogsBySearchCookies(logs, searches)
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

def testExtractingLogsByKeywords(logs, keywords):
    keywordDict = searchNProductLogsByKeywords(logs, keywords)
    for keyword, (searches, productLogs) in keywordDict.items():
        print(keyword, searches.count(), productLogs.count())

def makeJourney(searches, productLogs):
    logs = searches.union(productLogs).sortBy(lambda log: log[KEY_TIMESTAMP])
    journeys = logs.groupBy(lambda log: log[KEY_PERSISTENT_COOKIE]).map(lambda log: (log[0], list(log[1]))).collect()
    #for cookie, journey in journeys:
    #    for log in journey:

    printLogs(logs)
    #logs = logs.groupBy(lambda log: log[KEY_PERSISTENT_COOKIE]).foreach(print)

def trackedJourneysByCookie(keywordDict):
    for keyword, (searches, productLogs) in keywordDict.items():
        makeJourney(searches, productLogs)

def isSameJourney(log, log2):
    same = False
    if KEY_USER_ID_FROM_COOKIE in log.keys() and KEY_USER_ID_FROM_COOKIE in log2.keys():
        same = log[KEY_USER_ID_FROM_COOKIE] == log2[KEY_USER_ID_FROM_COOKIE]
    if KEY_USER_ID in log.keys() and KEY_USER_ID in log2.keys():
        same = same or log[KEY_USER_ID] == log2[KEY_USER_ID]
    return same

def updateDistinctGroups(distinctGroups, nKey, cookie, session):
    newDistinctGroups = {}
    for dKey in distinctGroups.keys():
        if cookie in dKey:
            nKey = dKey + nKey
            newDistinctGroups[nKey] = distinctGroups[dKey] + session
            break
        else:
            newDistinctGroups[dKey] = distinctGroups[dKey]
    return newDistinctGroups
  
def groupTesta(logs):
    sessionsByCookie = logs.groupBy(lambda log: log[KEY_PERSISTENT_COOKIE]).map(lambda log: (log[0], list(log[1]))).collect()
    sessionsByCookie = {k: v for (k, v) in sessionsByCookie}
    sessionsByUIDC = logs.groupBy(lambda log: log[KEY_USER_ID_FROM_COOKIE]).map(lambda log: (log[0], list(log[1]))).collect()
    sessionsByUIDC = {k: v for (k, v) in sessionsByUIDC}
    sessionsByUID = logs.groupBy(lambda log: log[KEY_USER_ID]).map(lambda log: (log[0], list(log[1]))).collect()
    sessionsByUID = {k: v for (k, v) in sessionsByUID}
  
KEY_TRIBLE_IDS = '_trib'
def idSetter(log):
    if not KEY_USER_ID_FROM_COOKIE in log.keys():
        log[KEY_USER_ID_FROM_COOKIE] = log[KEY_PERSISTENT_COOKIE]
    if not KEY_USER_ID in log.keys():
        log[KEY_USER_ID] = log[KEY_PERSISTENT_COOKIE]
    log[KEY_TRIBLE_IDS] = (log[KEY_PERSISTENT_COOKIE], log[KEY_USER_ID_FROM_COOKIE], log[KEY_USER_ID])
    return log

def groupTest(logs):
    sessionsByCookie = logs.groupBy(lambda log: log[KEY_PERSISTENT_COOKIE]).map(lambda log: (log[0], list(log[1])))
    print_(sessionsByCookie.count())
    logs = logs.map(idSetter).collect()
    idSets = []
    sessions = []
    for log in logs:
        added = False
        for i in range(len(idSets)):
            for id in log[KEY_TRIBLE_IDS]:
                if id in idSets[i]:
                    sessions[i].append(log)
                    idSets[i].union(log[KEY_TRIBLE_IDS])
                    added = True
                    break
        if not added:
            sessions.append([log])
            idSets.append(set(log[KEY_TRIBLE_IDS]))
    print_(len(sessions))

def keywordsTests():
    filteredPath = joinPath(clickstreamFolder, 'part-r-00000_filtered')
    logs = getLogs(None, filteredPath, False)
    groupTest(logs)
    #keyword = 'tupperware'
    #keywordDict = searchNProductLogsByKeywords(logs, keyword)
    #trackedJourneysByCookie(keywordDict)

def iriTest():
    print_(refererParser('http%3A%2F%2Fwww.gittigidiyor.com%2Farama%2F%3Fk%3Dnike%2520%25C3%25A7ocuk%2520ayakkab%25C4%25B1'))

def runNewExtractionMethods():
    #filteringTest()
    keywordsTests()