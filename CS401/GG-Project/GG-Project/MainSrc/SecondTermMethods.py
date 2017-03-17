from LogProcesser.LogOperatorTests import *
from LogProcesser.LogAnalyzerTests import *

def runLogAnalyzerTests():
    #generateParsedTestFile()
    #logs = readParseLogs(joinPath(clickstreamFolder, TEST_LOGS_FILE))
    #logs = getLogs()
    logs = getAllLogs()
    #logs = evalJson(joinPath(clickstreamFolder, TEST_LOGS_FILE))
    #basicTests()
    #countTestsForTransposes(logs)
    #mapReduceTests(logs)
    #moduleTests(logs)
    #snippingTests(logs) 
    #idCookieTests(logs) 
    #cookieJourneyTest(logs)
    #cookieJourneyTest2(logs)
    #coloredLogPrintingTests(logs)
    #coloredJourneyPrintingTest(logs)
    #printingActionsTest(logs)
    logs = getAllLogs()

def run(): 
    newTest()