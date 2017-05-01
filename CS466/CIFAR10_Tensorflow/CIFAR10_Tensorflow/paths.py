from OutputLogger import OutputLogger
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
    
PYTHON_VERSION = sys.version_info[0]

gitDir = ''
allLogsPath = ''
if COMPUTERNAME == 'MSI': 
    gitDir = 'D:\\OneDrive\\Projects\\Assignment-Projects'
elif COMPUTERNAME == 'LM-IST-00UBFVH8':
    gitDir = '/Users/miek/Documents/Projects/Assignment-Projects'
else:
    gitDir = '/soe/cicekm/Projects/Assignment-Projects'

outputFileName = joinPath(gitDir, 'CS466/CIFAR10_Tensorflow/CIFAR10_Tensorflow/output.txt')