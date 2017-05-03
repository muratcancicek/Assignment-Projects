from MainSrc.OutputLogger import OutputLogger
import sys
import os

# Machine based
COMPUTERNAME = os.getenv('COMPUTERNAME') 

def joinPath(*args):
    return os.path.join(args[0], args[1])
    if isinstance(args[0], list): args = args[0]
    if len(args) < 1: return args
    else:
        path = args[0]
        for arg in args[1:]:
            os.path.join(path, arg)
        return path

def getAbsolutePath(fileName):
    script_dir = os.path.dirname(__file__) 
    return joinPath(script_dir, fileName)
PYTHON_VERSION = sys.version_info[0]

pulled = False
if PYTHON_VERSION == 3:
    import git
    def gitPull(gitDir):   
        if pulled: return
        g = git.cmd.Git(gitDir)
        global pulled
        pulled = True
        g.pull()
    
    def gitPush(gitDir):
        repo = git.Repo(gitDir)
        origin = repo.remote(name='origin')
        index = repo.index
        #author = git.Actor("Muratcan Cicek", "muratcancicek0@gmail.com")
        #committer = git.Actor("Muratcan Cicek", "muratcancicek0@gmail.com")
        # commit by commit message and author and committer
        index.commit("Auto-commit")
        origin.push()
        print('Pushed')
        sys.exit()
    
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

Day1_iPhone_6_DataFolder = joinPath(sparkFolder, 'Day1_iPhone_6_Data')
Day1_lg_g4_DataFolder = joinPath(sparkFolder, 'Day1_lg_g4_Data')
gitDir = ''
allLogsPath = ''
HDFSRootFolder = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/'
HDFSDataFolder = joinPath(HDFSRootFolder, 'data')

if COMPUTERNAME == 'MSI': 
    gitDir = 'D:\\OneDrive\\\Projects\\Assignment-Projects'
    allLogsPath = 'D:\\Slow_Storage\\Senior_Data\\session\\'
    #gitPush(gitDir)
elif COMPUTERNAME == 'LM-IST-00UBFVH8':
    gitDir = '/Users/miek/Documents/Projects/Assignment-Projects'
    allLogsPath = '/Users/miek/Documents/Projects/Senior_Data/session/'
else:
    gitDir = '/root/Projects/Assignment-Projects'
    #if PYTHON_VERSION == 3:
    #  gitPull(gitDir)
    allLogsPath = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/session/'
    Day1_iPhone_6_DataFolder = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/data/Day1_iPhone_6_Data'
    
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
if COMPUTERNAME == 'osldevptst02':
   allParsedLogsFolder = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/Parsed/'
entireDayParsedLogsFolder1 = joinPath(allParsedLogsFolder, entireDay1 + '_parsed')
entireDayParsedLogsFolder2 = joinPath(allParsedLogsFolder, entireDay2 + '_parsed')

allSparkParsedLogsFolder = joinPath(allParsedLogsFolder, 'Spark')
entireDaySparkParsedLogsFolder1 = joinPath(allSparkParsedLogsFolder, entireDay1)
entireDaySparkParsedLogsFolder2 = joinPath(allSparkParsedLogsFolder, entireDay2)

def setFolder2():
    allRawLogsfolder = entireDayRawLogsfolder2
    allParsedLogsFolder = entireDayParsedLogsFolder2

#setFolder2()
sys.stdout = OutputLogger(dataFolder) 
