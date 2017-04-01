from MainSrc.OutputLogger import OutputLogger
import sys
import os

# Machine based
COMPUTERNAME = os.getenv('COMPUTERNAME') 

def joinPath(prePath, path):
    return os.path.join(prePath, path)

def getAbsolutePath(fileName):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    return joinPath(script_dir, fileName)
   
dataFolder = getAbsolutePath('data')
#if COMPUTERNAME == 'osldevptst02':
#    dataFolder = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/data/data'

rankingFolder = joinPath(dataFolder, 'ranking')
clickstreamFolder = joinPath(rankingFolder, 'clickstream')
logInfoFolder = joinPath(rankingFolder, 'logInfo')

productToPointFolder = joinPath(dataFolder, 'productToPoint') + os.path.sep
commonFieldFolder = joinPath(productToPointFolder, 'commonFieldStatistics') + os.path.sep
valuesFolder = joinPath(commonFieldFolder, 'values') + os.path.sep
commonFolder = joinPath(productToPointFolder, 'common') + os.path.sep
specsFolder = joinPath(productToPointFolder, 'specs') + os.path.sep

sparkFolder = joinPath(dataFolder, 'spark') + os.path.sep
hdfsOutputFolder = sparkFolder

allLogsPath = ''
if COMPUTERNAME == 'MSI':
    allLogsPath = 'D:\\Slow_Storage\\Senior_Data\\session\\' 
elif COMPUTERNAME == 'L-IST-14500667':
    allLogsPath = 'C:\\session\\'
elif COMPUTERNAME == 'LM-IST-00UBFVH8':
    allLogsPath = '/Users/miek/Documents/Projects/Senior_Data/session/'
else:
    allLogsPath = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/session/'
    hdfsOutputFolder = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/data/'
    
    
entireDay1 = '2016-09-27'
entireDay2 = '2016-09-28'    
allRawLogsfolder = allLogsPath
if COMPUTERNAME == 'osldevptst02':
    entireDay1 = '2016-12-25'
    entireDay2 = '2016-12-26'  
else:
    allRawLogsfolder = joinPath(allLogsPath, 'Raw')
entireDayRawLogsfolder1 = joinPath(allRawLogsfolder, entireDay1)
entireDayRawLogsfolder2 = joinPath(allRawLogsfolder, entireDay2)

allParsedLogsFolder = joinPath(allLogsPath, 'Parsed')
entireDayParsedLogsFolder1 = joinPath(allParsedLogsFolder, entireDay1)
entireDayParsedLogsFolder2 = joinPath(allParsedLogsFolder, entireDay2)

allSparkParsedLogsFolder = joinPath(allParsedLogsFolder, 'Spark')
entireDaySparkParsedLogsFolder1 = joinPath(allSparkParsedLogsFolder, entireDay1)
entireDaySparkParsedLogsFolder2 = joinPath(allSparkParsedLogsFolder, entireDay2)

def setFolder2():
    allRawLogsfolder = entireDayRawLogsfolder2
    allParsedLogsFolder = entireDayParsedLogsFolder2

setFolder2()
sys.stdout = OutputLogger(dataFolder) 
