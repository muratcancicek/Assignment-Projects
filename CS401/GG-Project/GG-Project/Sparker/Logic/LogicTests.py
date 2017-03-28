from .ProductPreferrer import *

def getSampleJourney(logs):
    keyword = 'lg g4'#'iphone 6'# getKeywords()[1]
    return getJourneyByKeyword(logs, keyword)


def getIdsTest(logs):
    #journey = sc_().textFile(joinPath(sparkFolder, 'lg_g4_journey')).map(lambda l: eval(l)) 
    #getSampleJourney(logs)
    #journey.saveAsTextFile(joinPath(sparkFolder, 'lg_g4_journey'))
    journey = logs
    #printActions(journey)
    getInterestingIds(journey)