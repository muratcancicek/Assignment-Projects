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
    modules = getLogsColumnAsList('module', logs)
    print list(set(modules))
    paymentLogs, indices = getLogsWhereValue('payment', 'module', logs = logs)
    print len(paymentLogs), paymentLogs[0]
    selectedLogs, indices = getLogsWhereValue(['payment', 'newseasion', 'search', 'chart'], 'module', logs = logs)
    print len(selectedLogs), selectedLogs[0]
    pass
