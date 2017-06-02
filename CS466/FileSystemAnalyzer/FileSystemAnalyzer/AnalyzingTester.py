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
        return self.name + b'|' + self.type + b'|' + bytes(self.size) + b'|' + self.path

allFiles = [] 
def createFileObjects(dir):
    try:
        files = getFilesIn(dir)
        for filePath in files:
            allFiles.append(myFile(joinPath(dir, filePath)))
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

   output = open('musicFolder_test.csv', 'w')
   output.write('type,count,total_size\n'.encode('utf-8'))
   for k, p in typeCounter.items():
       output.write((k + ',' + str(p[0]) + ',' + str(p[1]) + '\n').encode('utf-8'))