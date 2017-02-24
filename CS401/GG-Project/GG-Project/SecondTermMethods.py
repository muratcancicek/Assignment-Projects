from LogProcesser.LogAnalyzer import *
from LogProcesser.LogAnalyzerTests import *
from Printing import *

def run(): 
    #generateParsedTestFile()
    #logs = readParseLogs(joinPath(clickstreamFolder, TEST_LOGS_FILE))
    logs = getLogs()
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
    printingActionsTest(logs)
    newTest(logs)