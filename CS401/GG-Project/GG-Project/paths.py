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
entireDayRawLogsfolder = 'D:\\Slow_Storage\\Senior_Data\\session\\Raw\\2016-09-27\\'
allRawLogsfolder = entireDayRawLogsfolder

entireDayParsedLogsFolder = 'D:\\Slow_Storage\\Senior_Data\\session\\Parsed\\2016-09-27\\'
allParsedLogsFolder = entireDayParsedLogsFolder
