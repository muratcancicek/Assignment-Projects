import os
import sys

def joinPath(prePath, path):
    return os.path.join(prePath, path)

def getAbsolutePath(fileName):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    return joinPath(script_dir, fileName)
   
dataFolder = getAbsolutePath('data')

rankingFolder = joinPath(dataFolder, 'ranking')
clickstreamFolder = joinPath(rankingFolder, 'clickstream')
logInfoFolder = joinPath(rankingFolder, 'logInfo')

productToPointFolder = joinPath(dataFolder, 'productToPoint') + os.path.sep
commonFieldFolder = joinPath(productToPointFolder, 'commonFieldStatistics') + os.path.sep
valuesFolder = joinPath(commonFieldFolder, 'values') + os.path.sep
commonFolder = joinPath(productToPointFolder, 'common') + os.path.sep
specsFolder = joinPath(productToPointFolder, 'specs') + os.path.sep

# ON MSI 
allRawLogsfolder = 'D:\\Slow_Storage\\Senior_Data\\session\\Raw\\'
entireDayRawLogsfolder1 = joinPath(allRawLogsfolder, '2016-09-27')
entireDayRawLogsfolder2 = joinPath(allRawLogsfolder, '2016-09-28')

allParsedLogsFolder = 'D:\\Slow_Storage\\Senior_Data\\session\\Parsed\\'
entireDayParsedLogsFolder1 = joinPath(allParsedLogsFolder, '2016-09-27')
entireDayParsedLogsFolder2 = joinPath(allParsedLogsFolder, '2016-09-28')

def setFolder2():
    allRawLogsfolder = entireDayRawLogsfolder2
    allParsedLogsFolder = entireDayParsedLogsFolder2

setFolder2()

import time
from datetime import datetime
def nowStr():
    return str(datetime.now())