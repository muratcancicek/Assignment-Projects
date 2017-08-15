from paths import *
from PythonVersionHandler import *
from BotFilter import *
from Sessionizer import *
from ReadyTests import *
from ReadyTests2 import *
from FinalizedRunners import *
from SearchExtractor import *
from NewProductPreferrer import *
from SparkLogReader import *
from SparkLogFileHandler import *
from StringUtil import *

def may17ExtractionTest(day):
    dateStr = '2017-05-' + str(day)
    import paths, FinalizedRunners
    inputPath = paths.joinPath(may2017Folder, dateStr)
    keywords = get32Keywords()
    outputPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    FinalizedRunners.saveExtractedLogsByKeywordsFromHDFS(inputPath, keywords, outputPath)

def pairingTest(day):
    keywords = 'zigon sehpa' # get32Keywords() # 'iphone 7' # "BEKO 9 KG CAMASIR MAKINESI" # 'tupperware' # get5Keywords() # _file_old
    dateStr = '2017-05-' + str(day)
    import paths, SparkLogFileHandler, FinalizedRunners
    extractedPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    outputFolder = paths.joinPath(labeledPairsMayFromMayFolder, dateStr)
    FinalizedRunners.pairLabellingFromObjectiveLogsTest(extractedPath, keywords, outputFolder, filtering = False)

def runNewExtractionMethods():
    #may17ExtractionTest(21)
    #printAct(16)
    #joinTests()
    #coalesceAll([16, 18, 19], 24)
    pairingTest(17)