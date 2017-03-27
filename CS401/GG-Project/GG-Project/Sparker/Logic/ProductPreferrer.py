from Sparker.SparkLogProcesser.SparkLogAnalyzer import *
from Sparker.SparkLogProcesser.SparkLogOperator import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from MainSrc.PythonVersionHandler import *
from Sparker.PySparkImports import *

def getListedIdsFromJourney(Journey):
    searches = Journey.filter(isSearchLog)
    ids = getSnippedLogs(['ids'], searches)
    ids.foreach(print_)