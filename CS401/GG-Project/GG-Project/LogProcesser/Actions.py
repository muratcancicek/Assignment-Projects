#from LogAnalyzer import *
import LogAnalyzer as LA

class Action:
    PRODUCT_REFRESHED = 111 
    PRODUCT_CLICKED_LAST_SEARCH = 1
    PRODUCT_CLICKED_PREVIOUS_SEARCH = 2
    PRODUCT_CLICKED_FROM_OTHER_SIDE = 222
    PRODUCT_CART_LAST_SEARCH = 3
    PRODUCT_CART_PREVIOUS_SEARCH = 4
    PRODUCT_CART_FROM_OTHER_SIDE = 444
    PRODUCT_PAID_LAST_SEARCH = 5
    PRODUCT_PAID_PREVIOUS_SEARCH = 6
    PRODUCT_PAID_FROM_OTHER_SIDE = 666
    SEARCH_NEW = 7
    SEARCH_ORDER_CHANGED = 8
    SEARCH_NEXT_PAGE = 9
    SEARCH_PREVIOUS_PAGE = 10
    SEARCH_CATEGORY_SET = 11
    SEARCH_CATEGORY_UNSET = 12
    SEARCH_REFRESHED = 13
    SEARCH_EXTENDED = 14
    SEARCH_NARROWED = 15

def isProductClickedAfterSearch(previousLog, currentLog):
    return LA.isProductLog(currentLog) and LA.isSearchLog(previousLog)

def getActionForProductLog(log, productIndex, lastSearchIndexWithId):
    action = Action.PRODUCT_CLICKED_LAST_SEARCH
    if lastSearchIndexWithId == -1 or productIndex == -1:
        action = Action.PRODUCT_CLICKED_FROM_OTHER_SIDE
        if log['module'] == 'payment':
            action = Action.PRODUCT_PAID_FROM_OTHER_SIDE
        elif log['module'] == 'cart':
            action = Action.PRODUCT_CART_FROM_OTHER_SIDE
    if lastSearchIndexWithId == 0:
        action = Action.PRODUCT_CLICKED_LAST_SEARCH
        if log['module'] == 'payment':
            action = Action.PRODUCT_PAID_LAST_SEARCH
        elif log['module'] == 'cart':
            action = Action.PRODUCT_CART_LAST_SEARCH
    else:
        action = Action.PRODUCT_CLICKED_PREVIOUS_SEARCH
        if log['module'] == 'payment':
            action = Action.PRODUCT_PAID_PREVIOUS_SEARCH
        elif log['module'] == 'cart':
            action = Action.PRODUCT_CART_PREVIOUS_SEARCH
    return action

def getActionStringForProductLog(log, productIndex, lastSearchIndexWithId):
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

def getActionForSearch(search, previousLog):
    action = Action.SEARCH_NEW
    if previousLog == None or not LA.isSearchLog(previousLog):
        action = Action.SEARCH_NEW
    elif search['orderBy'] != previousLog['orderBy']:
        action = Action.SEARCH_ORDER_CHANGED
    elif search['pageNum'] > previousLog['pageNum']:
        action = Action.SEARCH_NEXT_PAGE
    elif search['pageNum'] < previousLog['pageNum']:
        action = Action.SEARCH_PREVIOUS_PAGE
    elif 'catCode' in search.keys() and not 'catCode' in previousLog.keys():
        action = Action.SEARCH_CATEGORY_SET
    elif not 'catCode' in search.keys() and 'catCode' in previousLog.keys():
        action = Action.SEARCH_CATEGORY_UNSET
    elif search['totfound'] > previousLog['totfound']:
        action = 'Page extended, ' + action
    elif search['totfound'] < previousLog['totfound']:
        action = 'Page narrowed, ' + action
    else:
        action = Action.SEARCH_REFRESHED
    return action 

def getActionStringForSearch(search, previousLog):
    action = 'Showing %i products with order %s on page %i for %s.'
    if previousLog == None or not LA.isSearchLog(previousLog):
        action = 'Searching, ' + action
    elif search['orderBy'] != previousLog['orderBy']:
        action = 'Order changed, ' + action
    elif search['pageNum'] > previousLog['pageNum']:
        action = 'Next Page, ' + action
    elif search['pageNum'] < previousLog['pageNum']:
        action = 'Previous Page, ' + action
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
            sentence = getActionStringForProductLog(currentLog, productIndex, lastSearchIndexWithId)
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