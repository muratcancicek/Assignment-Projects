from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.NewJourneyExtractor.SearchExtractor import *
from LogProcesser.scalaToPython.python_codes.LumberjackConstants import *
from Sparker.NewJourneyExtractor.Sessionizer import *

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

def specificPreviousSearches(productLog, search):
    previous = search[KEY_TIMESTAMP] < productLog[KEY_TIMESTAMP]
    session = False
    for id in log[KEY_FOUR_IDS]:
        if id in search[KEY_FOUR_IDS]:
            session = True
            break
    return previous and session

def findProductIdOnSearches(productLog, searches):
    searches = searches.filter(lambda search: specificPreviousSearches(productLog, search))

def trainingInstances(logs):
    (searches, viewedProductLogs, cartedOrPaidProductLogs) = logs
    searches = searches.map(idSetter)
    viewedProductLogs = viewedProductLogs.map(idSetter)
    cartedOrPaidProductLogs = cartedOrPaidProductLogs.map(idSetter)
    
    for productLogs in [viewedProductLogs, cartedOrPaidProductLogs]:
        productLogs = productLogs.collect()
        for product_log in productLogs: