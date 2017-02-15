from LogProcesser.LogAnalyzer import *
from LogProcesser.LogAnalyzerTests import *

def run(): 
    basicTests()
    logs = getLogs()
    countTestsForTransposes(logs)
    mapReduceTests(logs)
    newTest(logs)