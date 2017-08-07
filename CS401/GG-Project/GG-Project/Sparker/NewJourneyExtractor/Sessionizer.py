from MainSrc.PythonVersionHandler import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from LogProcesser.scalaToPython.python_codes.LumberjackConstants import *

KEY_FOUR_IDS = '_trib'
KEY_ORIGINAL_PERSISTENT_COOKIE = '__c'

def idSetter(log):
    log[KEY_ORIGINAL_PERSISTENT_COOKIE] = log[KEY_PERSISTENT_COOKIE]
    if not KEY_USER_ID_FROM_COOKIE in log.keys():
        log[KEY_USER_ID_FROM_COOKIE] = log[KEY_PERSISTENT_COOKIE]
    if not KEY_SESSION_ID in log.keys():
        log[KEY_SESSION_ID] = log[KEY_PERSISTENT_COOKIE]
    if not KEY_USER_ID in log.keys():
        log[KEY_USER_ID] = log[KEY_PERSISTENT_COOKIE]
    log[KEY_FOUR_IDS] = (log[KEY_PERSISTENT_COOKIE], log[KEY_USER_ID_FROM_COOKIE], log[KEY_USER_ID], log[KEY_SESSION_ID])
    return log

def sessionize(logs):
    if isinstance(logs, tuple):
        (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
        logs = searches.union(viewedProductLogs).union(cartedOrPaidProductLogs)
    logs = logs.map(idSetter).collect()
    idSets = []
    sessions = []
    for log in logs:
        added = False
        for i in range(len(idSets)):
            for id in log[KEY_FOUR_IDS]:
                if id in idSets[i]:
                    #print(69)
                    log[KEY_PERSISTENT_COOKIE] = str(i)
                    sessions[i].append(log)
                    idSets[i] = idSets[i].union(log[KEY_FOUR_IDS])
                    added = True
                    break
        if not added:
            l = len(sessions)
            log[KEY_PERSISTENT_COOKIE] =  str(l+1 if l > 0 else l)
            sessions.append([log])
            idSets.append(set(log[KEY_FOUR_IDS]))
    print_(len(sessions), 'sessions have been found')
    sessions = [sc_().parallelize(s) for s in sessions]
    return sessions

def sessionize2(logs):
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    searches = searches.map(idSetter)
    viewedProductLogs = viewedProductLogs.map(idSetter)
    cartedOrPaidProductLogs = cartedOrPaidProductLogs.map(idSetter)
    #views productLogs.

def preferredProducts(searches, productLogs):
    pass