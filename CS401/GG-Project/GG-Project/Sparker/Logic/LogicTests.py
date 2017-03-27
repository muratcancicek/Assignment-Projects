from Sparker.Logic.ProductPreferrer import *

def getSampleJourney(logs):
    keyword = getKeywords()[0]
    return getJourneyByKeyword(logs, keyword)


def getIdsTest(logs):
    keyword = getSampleJourney(logs)