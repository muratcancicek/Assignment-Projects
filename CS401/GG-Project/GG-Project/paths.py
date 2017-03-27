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

sparkFolder = joinPath(dataFolder, 'spark') + os.path.sep

# Machine based
COMPUTERNAME = os.getenv('COMPUTERNAME') 
allLogsPath = ''
if COMPUTERNAME == 'MSI':
    allLogsPath = 'D:\\Slow_Storage\\Senior_Data\\session\\' 
elif COMPUTERNAME == 'L-IST-14500667':
    allLogsPath = 'C:\\session\\'
elif COMPUTERNAME == 'LM-IST-00UBFVH8':
    allLogsPath = '/Users/miek/Documents/Projects/Senior_Data/session/'

allRawLogsfolder = joinPath(allLogsPath, 'Raw')
entireDayRawLogsfolder1 = joinPath(allRawLogsfolder, '2016-09-27')
entireDayRawLogsfolder2 = joinPath(allRawLogsfolder, '2016-09-28')

allParsedLogsFolder = joinPath(allLogsPath, 'Parsed')
entireDayParsedLogsFolder1 = joinPath(allParsedLogsFolder, '2016-09-27')
entireDayParsedLogsFolder2 = joinPath(allParsedLogsFolder, '2016-09-28')

allSparkParsedLogsFolder = joinPath(allParsedLogsFolder, 'Spark')
entireDaySparkParsedLogsFolder1 = joinPath(allSparkParsedLogsFolder, '2016-09-27')
entireDaySparkParsedLogsFolder2 = joinPath(allSparkParsedLogsFolder, '2016-09-28')

def setFolder2():
    allRawLogsfolder = entireDayRawLogsfolder2
    allParsedLogsFolder = entireDayParsedLogsFolder2

setFolder2()

#   cd /Users/miek/Documents/Projects/Assignment-Projects/CS401/GG-Project/GG-Project/
#   sshpass -p 'eBay@2017' ssh miek@127.0.0.1 
#   sshpass -p 'eBay@2017' ssh miek@10.200.133.227
#   sshpass -p 3022 'eBay@2017' ssh miek@10.200.133.227
#   shh -p 22 miek@10.200.133.227   
#   10.200.133.227:5900
#   ssh root@osldevptst02.host.gittigidiyor.net     F!T(9D2m
#   export SPARK_HOME="/opt/spark"