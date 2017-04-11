from paths import *

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

def printFilesTest():
    #subFoldersubFolderss = getSubDirs(musicFolder)
    traverseDirTree(musicFolder, countFiles)


def runtraverseMusicTest():
    printFilesTest()