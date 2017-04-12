from SystemHelpers.OutputLogger import OutputLogger
import sys
import os
import git

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

pulled = False
def gitPull(gitDir):   
    if pulled: return
    g = git.cmd.Git(gitDir)
    g.pull()    
    
dataFolder = getAbsolutePath('data')
notesFolder = joinPath(dataFolder, 'Notes')
extractorFolder = getAbsolutePath('Extractor')
extractorExe = joinPath(extractorFolder, 'streaming_extractor_music.exe')

first_outputs = joinPath(dataFolder, 'first_outputs')

musicFolder = 'D:\\OneDrive\\Music\\'
trainDataFolder = 'D:\\OneDrive\\Projects\\Fizy_Project\\Acoustic_Features_of_My_Music\\'

gitDir = ''
if COMPUTERNAME == 'MSI': 
    gitDir = 'D:\\OneDrive\\\Projects\\Assignment-Projects'
    #gitPush(gitDir)
elif COMPUTERNAME == 'LM-IST-00UBFVH8':
    gitDir = '/Users/miek/Documents/Projects/Assignment-Projects'
else:
    gitDir = '/root/Projects/Assignment-Projects'

sys.stdout = OutputLogger(notesFolder) 

from SystemHelpers.PythonVersionHandler import *
from SystemHelpers.Printing import *

def unique(list1):
    return list(set(list1))