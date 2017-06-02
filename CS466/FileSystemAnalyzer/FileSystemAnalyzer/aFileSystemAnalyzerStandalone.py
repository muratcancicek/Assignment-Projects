from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
import time
import sys
import os


outputFileName = 'FileSystemAnalyzerStandalone_output.txt'

def print_(*args):
    line = ''
    for ar in args:
        line += str(ar) + ' '
    line = line[:-1]+'\n'
    sys.stdout.write(line)
    if os.path.isfile(outputFileName):
        open(outputFileName, 'a').write(line)  
    else:
        open(outputFileName, 'w').write(line)  

def myXrange(i):
    if PYTHON_VERSION == 2:
        return xrange(i)
    else:
        return range(i)
        
def nowStr():
    return str(datetime.now())

# Machine based
COMPUTERNAME = os.getenv('COMPUTERNAME') 
if COMPUTERNAME == None: COMPUTERNAME = 'a strange computer'

def joinPath(*args):
    return os.path.join(args[0], args[1])
    if isinstance(args[0], list): args = args[0]
    if len(args) < 1: return args
    else:
        path = args[0]
        for arg in args[1:]:
            os.path.join(path, arg)
        return path
    
PYTHON_VERSION = sys.version_info[0]

def listDir(dir):
    try:
        return os.listdir(dir)
    except PermissionError:
        return []

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
    return path.split(os.path.sep)[-1].split('.')[-1].lower()

def getFileName(path):
    return path.split(os.path.sep)[-1].split('.')[0].lower()

def getFileSize(path):
    return os.path.getsize(path)

def listFileTypes(dir):
    files = getFilesIn(dir)
    types = [getFileType(file) for file in files]#unique()
    allTypes.extend(types)
    #print_(dir, '=', len(types), types)
    
class myFile(object):
    def __init__(self, path):
        self.path = path
        self.type = getFileType(path)
        self.name = getFileName(path)
        self.size = getFileSize(path)
        
    def __str__(self):
        return 'n: ' + self.name + ', t:' + self.type + ', s:' + str(self.size) + ', p:' + self.path
        
    def toRow(self):
        return self.name + b'|' + self.type + b'|' + bytes(self.size) + b'|' + self.path

allFiles = [] 
c = 0
def createFileObjects(dir):
    try:
        files = getFilesIn(dir)
        for filePath in files:
            allFiles.append(myFile(joinPath(dir, filePath)))
            global c
            c += 1
            if c != 0 and c % 1000 == 0:
                print_(c, 'files has been counted')
    except PermissionError:
        pass

def runTests():
   traverseDirTree('C:\\', createFileObjects)
   traverseDirTree('D:\\', createFileObjects)
   typeCounter = {}
   for f in allFiles:
       if f.type in typeCounter.keys():
           typeCounter[f.type][0] += 1
           typeCounter[f.type][1] += f.size
       else:
           typeCounter[f.type] = [1, f.size]

   output = open('Folder_test.csv', 'wb')
   output.write('type,count,total_size\n'.encode('utf-8'))
   for k, p in typeCounter.items():
       output.write((k + ',' + str(p[0]) + ',' + str(p[1]) + '\n').encode('utf-8'))

def printSeparater():
    for n in range(3):
        print_('#' * 88)
        
def main(method = None):
    printSeparater()
    print_('%s:' % nowStr(), 'Running on', COMPUTERNAME + '...')
    
    if method == None:
        runTests()
    else:
        method()

    print_('%s:' % nowStr(), 'DONE')
    printSeparater()

    if COMPUTERNAME == 'MSI' or COMPUTERNAME == 'LM-IST-00UBFVH8':
        sys.exit() 

if __name__ == "__main__":
    main()