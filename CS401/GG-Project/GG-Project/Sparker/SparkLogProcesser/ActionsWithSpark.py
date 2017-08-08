from MainSrc.PythonVersionHandler import *
#from LogAnalyzer import *
from . import SparkLogAnalyzer as LA
from LogProcesser.scalaToPython.python_codes.LumberjackParser import *

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
    title = (' (%s)' % (log['title'])) if 'title' in log.keys() else ''
    action = 'clicked%s.'
    if log['module'] == 'payment':
        action = 'paid%s.'
    elif log['module'] == 'cart':
        action = 'added to the cart%s.'
    sentence = 'Product with id %s %s%s'
    if lastSearchIndexWithId == -1 or productIndex == -1:
        try:
            return sentence % (int(log['id']), action % (' not from the searches so far'), title)
        except ValueError:
            li = [int(i) for i in log['id'].split('%7C')]
            return sentence % (int(li[0]), action % (' or ' + str(li[1:]) + ' not from the searches so far'), title)
    sentence = '%i. ' + sentence
    if lastSearchIndexWithId == 0:
        action = action % ('')
    else:
        action = action % (' from the recent %i. search' % (lastSearchIndexWithId + 1))
    return sentence % (productIndex + 1, str(log['id']), action, title)

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
    elif int(search['totfound']) > int(previousLog['totfound']):
        action = 'Page extended, ' + action
    elif int(search['totfound']) < int(previousLog['totfound']):
        action = 'Page narrowed, ' + action
    else:
        action = Action.SEARCH_REFRESHED
    return action 

def getActionStringForSearch(search, previousLog):
    action = 'Showing %i products with order %s on page %i for %s.'
    if previousLog == None or not LA.isSearchLog(previousLog):
        action = 'Searching, ' + action
    elif 'orderBy' in search.keys() and 'orderBy' in previousLog.keys() \
        and search['orderBy'] != previousLog['orderBy']:
        action = 'Order changed, ' + action
    elif 'pageNum' in search.keys() and 'pageNum' in previousLog.keys() \
        and search['pageNum'] > previousLog['pageNum']:
        action = 'Next Page, ' + action
    elif 'pageNum' in search.keys() and 'pageNum' in previousLog.keys() \
        and search['pageNum'] < previousLog['pageNum']:
        action = 'Previous Page, ' + action
    elif 'catCode' in search.keys() and not 'catCode' in previousLog.keys():
        action = ('Category set as %s, ' % search['catCode']) + action
    elif 'catCode' in search.keys() and 'catCode' in previousLog.keys() \
        and not 'catCode' in search.keys() and 'catCode' in previousLog.keys():
        action = 'Category unset, ' + action
    elif 'totfound' in search.keys() and 'totfound' in previousLog.keys() \
        and str(search['totfound']) > str(previousLog['totfound']):
        action = 'Page extended, ' + action
    elif 'totfound' in search.keys() and 'totfound' in previousLog.keys() \
        and str(search['totfound']) < str(previousLog['totfound']):
        action = 'Page narrowed, ' + action
    else:
        action = 'Refreshed, ' + action
    ids = len(search['ids']) if 'ids' in search.keys() else 0
    order = search['orderBy'] if 'orderBy' in search.keys() else 'None'
    pageNum = search['pageNum'] if 'pageNum' in search.keys() else -1
    keyword = search['keyword'] if 'keyword' in search.keys() else 'None'
    return action % (ids, order, pageNum, keyword)

def findProductIdOnSearches(currentLog, previousJourney):
    lastSearchIndexWithId, productIndex = -1, -1
    previousJourney.reverse()
    count = -1
    for pl in previousJourney:
        if LA.isSearchLog(pl):
            count += 1
            if isinstance(currentLog[KEY_ID], int):
                for t, jd in enumerate(pl[KEY_ID_LIST]):
                    if currentLog[KEY_ID] == jd:
                        return count, t
            elif isinstance(currentLog[KEY_ID], str):
                if '%7C' in currentLog[KEY_ID]:
                    processedIds = [int(i) for i in currentLog[KEY_ID].split('%7C')]
                    for t, jd in enumerate(pl[KEY_ID_LIST]):
                        if jd in processedIds:
                            return count, t
    return lastSearchIndexWithId, productIndex 

def getActionString(i, logs, showDetails = False):
    previousLog = logs[i-1] if i > 0 else None   
    currentLog = logs[i]
    previousJourney = logs[:i] #filter(lambda iLog: iLog[0] < i) 
    sentence = '' 
    if LA.cookieChanged(previousLog, currentLog):
        print_(LA.green('COOKIE CHANGED.'))
    if LA.isProductLog(currentLog): 
        lastSearchIndexWithId, productIndex = findProductIdOnSearches(currentLog, previousJourney)
        sentence = getActionStringForProductLog(currentLog, productIndex, lastSearchIndexWithId)
    elif LA.isSearchLog(currentLog):
             sentence = getActionStringForSearch(currentLog, previousLog)
    else:
        sentence = currentLog['module'] + '.'
    if showDetails:
        sentence = currentLog['time'] + ': ' + sentence
        if '_c' in list(currentLog.keys()):
            sentence = sentence[:-1] + ' for cookie ' + currentLog['_c'] + '.'
        
    return sentence  

def printAction(i, logs, color, showDetails = False):
    actionString = getActionString(i, logs, showDetails)
    if color == None:
        print_(actionString)
    else:
        print_(color(actionString))