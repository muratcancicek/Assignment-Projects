from LogProcesser.LogAnalyzer import *
import datetime

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
    snippedLogs = getSnippedLogs(["_bot", "_c", "_ip", "_t", 'module', 'sid', "timestamp", "uid", "uidc"], logs)
    subTranspose = getSubTranspose(["_bot", "_c", "_ip", "_t", 'module', 'sid', "timestamp", "uid", "uidc"], logs)
    print totalCounts, '\n', valueCounts, '\n', len(snippedLogs), '\n', len(subTranspose)
    
def mapReduceTests(logs = None): # Running successfully
    logs = getLogs(logs)
    modules = getLogsColumnAsList('module', logs)
    print modules
    abvars = getLogsColumnAsList('abvar', logs)
    print abvars
    selectedLogs, indices = getLogsWhereValue('payment', 'module', logs = logs)
    print len(selectedLogs), selectedLogs[0]
    sampleIp = '0a1c08fb8c90f2eb0ba27b1ba96c45546891aa3dc10a9cc45fc1cdceb47d29b2'
    sampleIp2 = '06bd3ecc3b6f4bbf4914918a9fe340c2bcafc0b3415a70526b79b02dd5884a83'
    selectedLogs, indices = getLogsWhereValue(sampleIp, logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs, indices = getLogsWhereValue(sampleIp, '_ip', logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs, indices = getLogsWhereValue([sampleIp, sampleIp2], logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs, indices = getLogsWhereValue([sampleIp, sampleIp2], '_ip', logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs, indices = getLogsWhere({'_ip': sampleIp, "abvar": "BMF2%2CMPO2"}, logs = logs)
    print len(selectedLogs), selectedLogs[0]
    selectedLogs, indices = getLogsWhere({'_ip': sampleIp, "abvar": ["BMF2%2CMPO2", 'BMF2%2CMPO2%2CRCP6']}, logs = logs)
    print len(selectedLogs), selectedLogs[0]
    
def newTest(logs = None): # Under development 
    logs = getLogs(logs)
    #modules = getLogsColumnAsList('module', logs)
    #print list(set(modules))
    paymentLogs, indices = getLogsWhereValue('payment', 'module', logs = logs)
    searchLogs, indices = getLogsWhereValue('search', 'module', logs = logs)
    itemLogs, indices = getLogsWhereValue('item', 'module', logs = logs)
    cartLogs, indices = getLogsWhereValue('cart', 'module', logs = logs)
    print len(paymentLogs), len(searchLogs), len(itemLogs), len(cartLogs)
    for log in searchLogs:
        if 'ids' in log.keys():
            log['ids'] = log['ids'].split('%2C')
        else:
          searchLogs.remove(log)
   
    paymentIds = [log['id'] for log in paymentLogs]
    
    #for log in cartLogs :
    #    print log
   
    cookies = [log['_c'] for log in cartLogs]
    cookiesSet = list(set(cookies))
    print len(cookies) , len(cookiesSet) 

    for cookie in cookiesSet:
        cookies.remove(cookie)

    #for cookie in cookies:
    #    print(cookie)

    print  len(paymentIds)
    cartIds = [log['id'] for log in cartLogs]
    
    print len(cartIds)
    commonIds = [id for id in paymentIds if id in cartIds]
    print len( commonIds)

    paymentCookies = []

    for paymentLog in paymentLogs:
        paymentCookies.append({'id':paymentLog['id'], '_c': paymentLog['_c']}) 
        #print paymentLog['id'], paymentLog['_c']
    myLogs = []
    
    for paymentLog in paymentCookies:
        for log in searchLogs+itemLogs+cartLogs+paymentLogs:
            if log["module"] =="search": 
                if '_c' in log.keys():
                    if 'ids' in log.keys() and paymentLog['id'] in log['ids'] and paymentLog["_c"] == log["_c"]:
                        myLogs.append(log) 
                else:
                    if 'ids' in log.keys() and paymentLog['id'] in log['ids']:
                        myLogs.append(log) 
            else:
                if '_c' in log.keys():
                    if 'id' in log.keys() and paymentLog['id'] == log['id'] and paymentLog["_c"] == log["_c"]:
                        myLogs.append(log) 
                else:
                    if 'id' in log.keys() and paymentLog['id'] == log['id']:
                        myLogs.append(log)
       


    
    for log in myLogs :
        if  '_c' in log.keys() and log["_c"]=="9b3c7d6da4fbae9a258c36f8bb9bb40e8d29d963547a539ddd2e998336daf234":
            log["time"] = datetime.datetime.fromtimestamp(int(log["timestamp"])/ 1e3) 
            print log["time"]
            print log

    


    #for log 
    #selectedLogs, indices = getLogsWhereValue(['payment', 'newseasion', 'search', 'chart'], 'module', logs = logs)
    #print len(selectedLogs), selectedLogs[0]
    #pass
