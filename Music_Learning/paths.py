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

Fizy_Project_OfflineFolder = 'D:\\OneDrive\\Projects\\Fizy_Project\\'
AcousticFeaturesFolder = joinPath(dataFolder, 'AcousticFeatures')
Acoustic_Features_OfflineFolder = joinPath(Fizy_Project_OfflineFolder, 'Acoustic_Features_Offline')
first_outputs = joinPath(dataFolder, 'first_outputs')

musicFolder = 'D:\\OneDrive\\Music\\'
trainDataFolder = joinPath(Fizy_Project_OfflineFolder, 'Acoustic_Features_of_My_Music')

gitDir = ''
if COMPUTERNAME == 'MSI': 
    gitDir = 'D:\\OneDrive\\Projects\\Assignment-Projects'
    trainDataFolder = 'D:\\OneDrive\\Projects\\Fizy_Project\\Acoustic_Features_of_My_Music\\'
    #joinPath(Fizy_Project_OfflineFolder, 'Acoustic_Features_of_My_Music')
    #gitPush(gitDir)
elif COMPUTERNAME == 'LM-IST-00UBFVH8':
    gitDir = '/Users/miek/Documents/Projects/Assignment-Projects/'
    musicFolder = '/Users/miek/Documents/Music/'
    Fizy_Project_OfflineFolder = '/Users/miek/Documents/Projects/Music/Fizy_Project/'
    Acoustic_Features_OfflineFolder = joinPath(Fizy_Project_OfflineFolder, 'Acoustic_Features_Offline')
    trainDataFolder = joinPath(Fizy_Project_OfflineFolder, 'Acoustic_Features_of_My_Music')
else:
    gitDir = '/root/Projects/Assignment-Projects'

sys.stdout = OutputLogger(notesFolder) 

from SystemHelpers.PythonVersionHandler import *
from SystemHelpers.StringUtil import *
from SystemHelpers.Printing import *

def unique(list1):
    return list(set(list1))