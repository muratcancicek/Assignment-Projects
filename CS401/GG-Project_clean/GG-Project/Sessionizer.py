from PythonVersionHandler import *
from SearchExtractor import *
from SparkLogFileHandler import *
from LumberjackConstants import *

KEY_FOUR_IDS = '_trib'
KEY_ORIGINAL_PERSISTENT_COOKIE = '__c'

cookieCounter = 0
def idSetter(log):
    if not KEY_PERSISTENT_COOKIE in log.keys():
        global cookieCounter
        log[KEY_PERSISTENT_COOKIE] = cookieCounter
        cookieCounter += 1
    log[KEY_ORIGINAL_PERSISTENT_COOKIE] = log[KEY_PERSISTENT_COOKIE]
    if not KEY_USER_ID_FROM_COOKIE in log.keys():
        log[KEY_USER_ID_FROM_COOKIE] = log[KEY_PERSISTENT_COOKIE]
    if not KEY_SESSION_ID in log.keys():
        log[KEY_SESSION_ID] = log[KEY_PERSISTENT_COOKIE]
    if not KEY_USER_ID in log.keys():
        log[KEY_USER_ID] = log[KEY_PERSISTENT_COOKIE]
    log[KEY_FOUR_IDS] = (log[KEY_PERSISTENT_COOKIE], log[KEY_USER_ID_FROM_COOKIE], log[KEY_USER_ID], log[KEY_SESSION_ID])
    return log

def getUsefulSessions(sessions):
    usefulSessions = []
    for s in sessions:
        se, pr = False, False
        for l in s:
            if isinstance(l, list):
                print_(l)
            if isProduct(l):
                if se:
                    usefulSessions.append(s)
                    break
                else: pr = True
            elif isSearch(l):
                if pr:
                    usefulSessions.append(s)
                    break
                else: se = True
    print_(len(usefulSessions), 'sessions have been found useful by', nowStr())
    usefulSessions = [sc_().parallelize(s) for s in usefulSessions]
    return usefulSessions

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
    print_(len(sessions), 'sessions have been found in total by', nowStr())
    return getUsefulSessions(sessions)

def sessionize2(logs):
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    searches = searches.map(idSetter)
    viewedProductLogs = viewedProductLogs.map(lambda vk: (vk[0], idSetter(vk[1])))
    cartedOrPaidProductLogs = cartedOrPaidProductLogs.map(lambda vk: (vk[0], idSetter(vk[1])))
    #views productLogs.

def preferredProducts(searches, productLogs):
    pass