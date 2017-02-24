#from LogAnalyzer import *
import LogAnalyzer as LA

def isProductClickedAfterSearch(previousLog, currentLog):
    return LA.isProductLog(currentLog) and LA.isSearchLog(previousLog)

def getActionStringForProduct(log, productIndex, lastSearchIndexWithId):
    action = 'clicked%s.'
    if log['module'] == 'payment':
        action = 'paid%s.'
    elif log['module'] == 'cart':
        action = 'added to the cart%s.'
    sentence = 'Product with id %i %s'
    if lastSearchIndexWithId == -1 or productIndex == -1:
        return sentence % (log['id'], action % (' not from the searches so far'))
    sentence = '%i. ' + sentence
    if lastSearchIndexWithId == 0:
        action = action % ('')
    else:
        action = action % (' from the recent %i. search' % (lastSearchIndexWithId + 1))
    return sentence % (productIndex, log['id'], action)

def getActionStringForSearch(search, previousLog):
    action = 'Showing %i products with order %s on page %i for %s.'
    if previousLog == None or not LA.isSearchLog(previousLog):
        action = 'Searching, ' + action
    elif search['orderBy'] != previousLog['orderBy']:
        action = 'Order changed, ' + action
    elif search['pageNum'] != previousLog['pageNum']:
        action = 'Page changed, ' + action
    elif 'catCode' in search.keys() and not 'catCode' in previousLog.keys():
        action = ('Category set as %s, ' % search['catCode']) + action
    elif not 'catCode' in search.keys() and 'catCode' in previousLog.keys():
        action = 'Category unset, ' + action
    elif search['totfound'] > previousLog['totfound']:
        action = 'Page extended, ' + action
    elif search['totfound'] < previousLog['totfound']:
        action = 'Page narrowed, ' + action
    else:
        action = 'Refreshed, ' + action
    return action % (len(search['ids']), search['orderBy'], search['pageNum'], search['keyword'])

def getActionString(i, logs, showDetails = False):
    searchIds = LA.getIdsFromSearches(logs[:i])
    previousLog = logs[i-1] if i > 0 else None   
    currentLog = logs[i]
    sentence = ''
    if LA.isProductLog(currentLog): 
        if currentLog['id'] in searchIds:
            lastSearchIndexWithId, productIndex = LA.findLastSearchContainsProduct(currentLog, logs[:i])
            sentence = getActionStringForProduct(currentLog, productIndex, lastSearchIndexWithId)
    elif LA.isSearchLog(currentLog):
             sentence = getActionStringForSearch(currentLog, previousLog)
    if showDetails:
        sentence = currentLog['time'] + ': ' + sentence
        if '_c' in currentLog.keys():
            sentence = sentence[:-1] + ' for cookie ' + currentLog['_c'] + '.'
    return sentence  

def printAction(i, logs, color, showDetails = False):
    actionString = getActionString(i, logs, showDetails)
    if color == None:
        print actionString
    else:
        print color(actionString)