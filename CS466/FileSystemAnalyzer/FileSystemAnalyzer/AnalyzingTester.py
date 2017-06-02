from FolderTraverser import *
from PythonVersionHandler import *
from paths import *

class myFile(object):
    def __init__(self, path):
        self.path = path
        self.type = getFileType(path)
        self.name = getFileName(path)
        self.size = getFileSize(path)
        
    def __str__(self):
        return 'n: ' + self.name + ', t:' + self.type + ', s:' + str(self.size) + ', p:' + self.path
        
    def toRow(self):
        return self.name + '|' + self.type + '|' + str(self.size) + '|' + self.path

allFiles = [] 
def createFileObjects(dir):
    files = getFilesIn(dir)
    for filePath in files:
        allFiles.append(myFile(joinPath(dir, filePath)))

def runTests():
   traverseDirTree(musicFolder, createFileObjects)
   for f in allFiles[-3:]:
       print_(f.toRow())