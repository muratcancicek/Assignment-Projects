#from LogAnalyzer import *
import LogAnalyzer as LA

def isProductClickedAfterSearch(previousLog, currentLog):
    return LA.isProductLog(currentLog) and LA.isSearchLog(previousLog)

def printAction(i, logs):
    searchIds = LA.getIdsFromSearches(logs[:i])
    if i > 0:
        previousLog = logs[i-1]
        currentLog = logs[i]
        #if isProductClickedAfterSearch(previousLog, currentLog): 
        if LA.isProductLog(currentLog): 
           if currentLog['id'] in searchIds:
               line = ''
               lastSearchIndexWithId, productIndex = LA.findLastSearchContainsProduct(currentLog, logs[:i])
               if lastSearchIndexWithId == -1 or productIndex == -1:
                   line = 'Product with id ' +  str(currentLog['id']) + ' not clicked from searches.'
               else:
                   line = str(productIndex) + '. Product with id ' + str(currentLog['id']) + \
                        ' clicked' + '.' if lastSearchIndexWithId == 0 else 'from the recent ' + \
                        str(lastSearchIndexWithId) + '. search.'
               print LA.pink(line)
