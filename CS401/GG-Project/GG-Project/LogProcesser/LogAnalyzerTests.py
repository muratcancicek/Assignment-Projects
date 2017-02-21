from LogProcesser.LogAnalyzer import *

def basicTests(): # Running successfully
    logs = readLogs(TEST_LOGS)
    log = logs[0]
    print log
    map = parseLog(log)
    print map
    print '\n', map['title']
    print '\n', map['module']
    #basicTests()

def countTestsForTransposes(logs = None):  # Running successfully
    logs = getLogs(logs)
    totalCounts, valueCounts = readCounts(logs)
    snippedLogs = getSnippedLogs(['_bot', '_c', '_ip', '_t', 'module', 'sid', 'timestamp', 'uid', 'uidc'], logs)
    subTranspose = getSubTranspose(['_bot', '_c', '_ip', '_t', 'module', 'sid', 'timestamp', 'uid', 'uidc'], logs)
    print totalCounts, '\n', valueCounts, '\n', len(snippedLogs), '\n', len(subTranspose)
    
def mapReduceTests(logs = None): # Running successfully
    logs = getLogs(logs)
    modules = getLogsColumnAsList('module', logs)
    print modules
    abvars = getLogsColumnAsList('abvar', logs)
    print abvars
    selectedLogs = getLogsWhereValue('payment', 'module', logs = logs)
    print len(selectedLogs), selectedLogs[0]
    sampleIp = '0a1c08fb8c90f2eb0ba27b1ba96c45546891aa3dc10a9cc45fc1cdceb47d29b2'
    sampleIp2 = '06bd3ecc3b6f4bbf4914918a9fe340c2bcafc0b3415a70526b79b02dd5884a83'
    selectedLogs = getLogsWhereValue(sampleIp, logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs = getLogsWhereValue(sampleIp, '_ip', logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs = getLogsWhereValue([sampleIp, sampleIp2], logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs = getLogsWhereValue([sampleIp, sampleIp2], '_ip', logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs = getLogsWhere({'_ip': sampleIp, 'abvar': 'BMF2%2CMPO2'}, logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs = getLogsWhere({'_ip': sampleIp, 'abvar': ['BMF2%2CMPO2', 'BMF2%2CMPO2%2CRCP6']}, logs = logs)
    print len(selectedLogs), selectedLogs[0]
    
def moduleTests(logs = None): # Running successfully
    logs = getLogs(logs)
    modules = getModuleMap(logs)
    print modules.keys()
    focusedModules = ['newsession', 'search', 'item' 'cart', 'payment']
    modules = getModuleMap(logs, focusedModules)
    print modules.keys()
    for module in modules.values():
        print module[0]
    counts = getModuleCounts(logs)
    print counts.items()
    modules = getModuleMap(logs)
    counts = getModuleCounts(modules)
    print counts.items()
    counts = getModuleCounts(modules, focusedModules)
    print counts.items()
    
def snippingTests(logs = None): # Running successfully
    logs = getLogs(logs)
    ids = getSnippedLogs('id', logs)
    print ids, '\n', len(ids)
    ids = getSnippedLogs(['id', '_c'], logs)
    print ids, '\n', len(ids)
    modules = getModuleMap(logs)
    ids = getSnippedLogs(['id', '_c'], modules['payment'])
    print ids, '\n', len(ids)

def idCookieTests(logs = None): # Running successfully
    logs = getLogs(logs)
    modules = getModuleMap(logs)   
    paymentIds = getLogsColumnAsList('id', modules['payment'])
    print len(modules['payment']), len(paymentIds) 
    print modules['payment'][0], '\n', paymentIds[0]
    #for log in modules['cart']:
    #    print log
    cookies = getLogsColumnAsList('_c', modules['cart'])
    cookiesSet = list(set(cookies))
    print len(cookies), len(cookiesSet) 
    for cookie in cookiesSet:
        cookies.remove(cookie)
    print len(cookies)

def cookieJourneyTest(logs = None, cookie = None): # Running successfully
    logs = getLogs(logs) 
    if cookie == None:  
        cookie = '9b3c7d6da4fbae9a258c36f8bb9bb40e8d29d963547a539ddd2e998336daf234'
    sampleJourney = getJourneyFromCookie(cookie, logs)
    for log in sampleJourney:
        print log['time']
        print log['module'], log
        
def cookieJourneyTest2(logs = None): # Under development 
    cookieJourneyTest(logs, '9b3c7d6da4fbae9a258c36f8bb9bb40e8d29d963547a539ddd2e998336daf234')

def newTest(logs = None): # Under development 
    logs = getLogs(logs) 
    modules = getModuleMap(logs)   
    keyword = 'lg g4'
    #sampleJourney = getLogsWhereValue(2, 'pageNum', modules['search'])
    sampleJourney = getLogsWhereValue(keyword, 'keyword', modules['search'])
    sampleJourney.sort(key = lambda log: log['timestamp'])    
    paymentCookies = getLogsColumnAsList('_c', modules['payment'])
    cartCookies = getLogsColumnAsList('_c', modules['cart'])    
    richCookies = list(set(paymentCookies+cartCookies))
    cookies = getLogsColumnAsList('_c', sampleJourney)
    cookies = list(set(cookies)) 
    print cookies
    print [c for c in richCookies if c in cookies]
    richCookies = list(set(paymentCookies+cartCookies)) 
    cookie = '9b3c7d6da4fbae9a258c36f8bb9bb40e8d29d963547a539ddd2e998336daf234'
    #sampleJourney = getLogsWhereValue(cookie, '_c', modules['cart'] + modules['payment'])
    #for log in modules['item']:
    #    for search in sampleJourney:
    #        if hasSearchThisItem(search, log):
    #            print 'item clicked', log['id'] 
    for log in modules['cart'] + modules['payment']:
        loved = False
        for search in sampleJourney:
            if hasSearchThisItem(search, log):
                print blue(search['time']), log['_c'], search
                loved = True
        if loved:
            print red(log['time']), log['id'], log['module'],  log['_c'], log
    #for log in sampleJourney:
    #    if '_c' in log.keys():
    #        print log['_c']
    #    else:
    #        print 'no cookie'
    for log in sampleJourney:
        print green(log['time']), log['_c'] if '_c' in log.keys() else None, log