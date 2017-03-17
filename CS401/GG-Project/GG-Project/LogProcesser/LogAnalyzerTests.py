from MainSrc.PythonVersionHandler import *
from .LogAnalyzer import *

def basicTests(): # Running successfully
    logs = readLogs(TEST_LOGS)
    log = logs[0]
    print_(log)
    map = parseLog(log)
    print_(map)
    print_('\n', map['title'])
    print_('\n', map['module'])
    #basicTests()

def countTestsForTransposes(logs = None):  # Running successfully
    logs = getLogs(logs)
    totalCounts, valueCounts = readCounts(logs)
    snippedLogs = getSnippedLogs(['_bot', '_c', '_ip', '_t', 'module', 'sid', 'timestamp', 'uid', 'uidc'], logs)
    subTranspose = getSubTranspose(['_bot', '_c', '_ip', '_t', 'module', 'sid', 'timestamp', 'uid', 'uidc'], logs)
    print_(totalCounts, '\n', valueCounts, '\n', len(snippedLogs), '\n', len(subTranspose))
    
def mapReduceTests(logs = None): # Running successfully
    logs = getLogs(logs)
    modules = getLogsColumnAsList('module', logs)
    print_(modules)
    abvars = getLogsColumnAsList('abvar', logs)
    print_(abvars)
    selectedLogs = getLogsWhereValue('payment', 'module', logs = logs)
    print_(len(selectedLogs), selectedLogs[0])
    sampleIp = '0a1c08fb8c90f2eb0ba27b1ba96c45546891aa3dc10a9cc45fc1cdceb47d29b2'
    sampleIp2 = '06bd3ecc3b6f4bbf4914918a9fe340c2bcafc0b3415a70526b79b02dd5884a83'
    selectedLogs = getLogsWhereValue(sampleIp, logs = logs)
    print_(len(selectedLogs), selectedLogs[0])
    selectedLogs = getLogsWhereValue(sampleIp, '_ip', logs = logs)
    print_(len(selectedLogs), selectedLogs[0])
    selectedLogs = getLogsWhereValue([sampleIp, sampleIp2], logs = logs)
    print_(len(selectedLogs), selectedLogs[0])
    selectedLogs = getLogsWhereValue([sampleIp, sampleIp2], '_ip', logs = logs)
    print_(len(selectedLogs), selectedLogs[0])
    selectedLogs = getLogsWhere({'_ip': sampleIp, 'abvar': 'BMF2%2CMPO2'}, logs = logs)
    print_(len(selectedLogs), selectedLogs[0])
    selectedLogs = getLogsWhere({'_ip': sampleIp, 'abvar': ['BMF2%2CMPO2', 'BMF2%2CMPO2%2CRCP6']}, logs = logs)
    print_(len(selectedLogs), selectedLogs[0])
    
def moduleTests(logs = None): # Running successfully
    logs = getLogs(logs)
    modules = getModuleMap(logs)
    print_(modules.keys())
    focusedModules = ['newsession', 'search', 'item' 'cart', 'payment']
    modules = getModuleMap(logs, focusedModules)
    print_(modules.keys())
    for module in modules.values():
        print_(module[0])
    counts = getModuleCounts(logs)
    print_(counts.items())
    modules = getModuleMap(logs)
    counts = getModuleCounts(modules)
    print_(counts.items())
    counts = getModuleCounts(modules, focusedModules)
    print_(counts.items())
    
def snippingTests(logs = None): # Running successfully
    logs = getLogs(logs)
    ids = getSnippedLogs('id', logs)
    print_(ids, '\n', len(ids))
    ids = getSnippedLogs(['id', '_c'], logs)
    print_(ids, '\n', len(ids))
    modules = getModuleMap(logs)
    ids = getSnippedLogs(['id', '_c'], modules['payment'])
    print_(ids, '\n', len(ids))

def idCookieTests(logs = None): # Running successfully
    logs = getLogs(logs)
    modules = getModuleMap(logs)   
    paymentIds = getLogsColumnAsList('id', modules['payment'])
    print_(len(modules['payment']), len(paymentIds))
    print_(modules['payment'][0], '\n', paymentIds[0])
    #for log in modules['cart']:
    #    print_(log
    cookies = getLogsColumnAsList('_c', modules['cart'])
    cookiesSet = list(set(cookies))
    print_(len(cookies), len(cookiesSet))
    for cookie in cookiesSet:
        cookies.remove(cookie)
    print_(len(cookies))

def cookieJourneyTest(logs = None, cookie = None): # Running successfully
    logs = getLogs(logs) 
    if cookie == None:  
        cookie = '9b3c7d6da4fbae9a258c36f8bb9bb40e8d29d963547a539ddd2e998336daf234'
    sampleJourney = getJourneyFromCookie(cookie, logs)
    for log in sampleJourney:
        print_(log['time'])
        print_(log['module'], log)
        
def cookieJourneyTest2(logs = None): # Under development 
    cookieJourneyTest(logs, '9b3c7d6da4fbae9a258c36f8bb9bb40e8d29d963547a539ddd2e998336daf234')
    
def coloredPrintingTests(): # Running successfully
    print_(red('po['), 9, blue('time'), 'kj')
    print_(red('po[') + str(9) + blue('time') + 'kj')
    print_(red('po[') + bcolors.DEFAULT + str(9) + blue('time') + bcolors.DEFAULT + 'kj')
    print_(bcolors.RED + 'po[' + str(9) + bcolors.BLUE + 'time' + 'kj')
    print_(bcolors.PINK + 'po[' + str(9) + bcolors.BLUE + 'time' + 'kj')
    print_(bcolors.PINK + 'po[' + bcolors.END + str(9) + bcolors.BLUE + 'time' + bcolors.END + 'kj')
    
def coloredLogPrintingTests(logs = None): # Running successfully
    logs = getLogs(logs) 
    log = logs[0]
    print_(logToStr(log))
    print_(logToStr(log, ['_c']))
    print_(logToStr(log, colorMap = {'time': red, '_c': blue}))
    
def coloredJourneyPrintingTest(logs = None): # Running successfully
    logs = getLogs(logs) 
    cookie = '9b3c7d6da4fbae9a258c36f8bb9bb40e8d29d963547a539ddd2e998336daf234'
    sampleJourney = getJourneyFromCookie(cookie, logs)
    printJourney(sampleJourney)

def journeyByKeywordTest(logs = None): # Running successfully
    logs = getLogs(logs) 
    keyword = 'lg g4'
    journey = getJourneyByKeyword(logs, keyword)
    printJourney(journey)

def printingActionsTest(logs = None): # Running successfully
    logs = getLogs(logs) 
    modules = getModuleMap(logs)   
    keyword = 'Lenovo 710'
    journey = getJourneyByKeyword(modules, keyword)
    print_('Printing logs as journey...')
    printLogs(journey)
    print_('Printing actions as journey...')
    printActions(journey)
    print_('Printing detailed journey...')
    printJourney(journey)