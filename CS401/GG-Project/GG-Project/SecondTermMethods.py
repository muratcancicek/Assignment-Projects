from LogProcesser.LogAnalyzer import *
from LogProcesser.LogAnalyzerTests import *

def run(): 
    logs = getLogs()
    #basicTests()
    #countTestsForTransposes(logs)
    #mapReduceTests(logs)
    newTest(logs)