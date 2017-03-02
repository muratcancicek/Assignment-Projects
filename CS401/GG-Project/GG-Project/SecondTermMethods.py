from LogProcesser.LogAnalyzer import *
from LogProcesser.LogAnalyzerTests import *
from Printing import *

#ALOT = 1e6
#vals = [max(min(x, ALOT), -ALOT) for x in (valueWI, valueHI, valueWF, valueHF)]
#dc.DrawLine(*vals)

def run(): 
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
    newTest(logs)