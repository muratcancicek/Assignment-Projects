from paths import *
from Extractor.ExtractorRunner import run as runExtractor 

def listDir(dir):
    return os.listdir(dir)

def isDir(path):
    return os.path.isdir(path)

def isSubDir(dir, item):
    return isDir(joinPath(dir, item))

def isFile(path):
    return os.path.isfile(path)

def isFileIn(dir, item):
    return isFile(joinPath(dir, item))

def getSubDirs(dir):
    return [item for item in listDir(dir) if isSubDir(dir, item)]

def getFilesIn(dir):
    return [item for item in listDir(dir) if isFileIn(dir, item)]
   
def printListVertical(list, indent = 0):
    indent = indent * '  '
    for item in list:  print_(indent + item)
    
def printDirTree(dir, indent = 0):
    indentStr = indent * '  '
    for subDir in getSubDirs(dir):  
        print_(indentStr + subDir)
        printDirTree(joinPath(dir, subDir), indent + 1)

def traverseDirTree(dir, method):
    method(dir)
    for subDir in getSubDirs(dir): 
        traverseDirTree(joinPath(dir, subDir), method)

def countFiles(dir):
    files = getFilesIn(dir)
    print_(dir, '=', len(files))
    
supportedTypes = ['mp4', 'mp3', 'm4a', 'wav']
allTypes = []
def getFileType(path):
    return path.split('.')[-1].lower()

def listFileTypes(dir):
    files = getFilesIn(dir)
    types = [getFileType(file) for file in files]#unique()
    allTypes.extend(types)
    #print_(dir, '=', len(types), types)

def makeTrainFolder(inputFolder, outputFolder):
    def makeFolder(dir):
        newFolder = getFixedEncodingValue(dir.replace(inputFolder, outputFolder))
        if not os.path.exists(newFolder):
            os.mkdir(newFolder)
    traverseDirTree(inputFolder, makeFolder)

def extractFeaturesFromFolder(inputFolder, outputFolder):
    def processFile(path):
        fileType = getFileType(path)
        if not fileType in supportedTypes: return
        features = path.replace(inputFolder, outputFolder).replace('.'+fileType, '.json')
        features = getFixedEncodingValue(features)
        if os.path.exists(features):
            print_(features, 'already exists, will be skipped.')
        else:
            try:
                path0 = path.encode('ascii')
            except UnicodeEncodeError:
                print_(features, 'has unicode problems, will be skipped.')
                return
            runExtractor(path,features)
         
    def processFolder(dir):
        newFolder = getFixedEncodingValue(dir.replace(inputFolder, outputFolder))
        if not os.path.exists(newFolder):
            os.mkdir(newFolder)
            print_(newFolder, 'cannot be found, will be created now.')
        for file in getFilesIn(dir):
            processFile(joinPath(dir, file))
    traverseDirTree(inputFolder, processFolder)
    
testInputFolder = 'D:\\OneDrive\Music\\Classical Music Top 100\\ncesaz_-_7_Yollar___Roads_2011mp3yolu.net\\İncesaz - 7 Yollar & Roads (2011)\\'
testOutputFolder = joinPath(trainDataFolder, 'Classical Music Top 100\\ncesaz_-_7_Yollar___Roads_2011mp3yolu.net\\İncesaz - 7 Yollar & Roads (2011)\\')
#testInputFolder = 'D:\\OneDrive\Music\\GWEN STEFANI\\'
#testOutputFolder = joinPath(trainDataFolder, 'GWEN STEFANI').replace('\\', '\\\\')[:87].encode( sys.getfilesystemencoding() 
def printFilesTest():
    #subFoldersubFolderss = getSubDirs(musicFolder)
    #traverseDirTree(musicFolder, listFileTypes)
    #print_({t: allTypes.count(t) for t in unique(allTypes) if t in supportedTypes})
    #makeTrainFolder(musicFolder, trainDataFolder)
    #print_('Acoustic features will be extracted.')
    #extractFeaturesFromFolder(testInputFolder, testOutputFolder)
    extractFeaturesFromFolder(musicFolder,trainDataFolder)

def runtraverseMusicTest():
    printFilesTest()