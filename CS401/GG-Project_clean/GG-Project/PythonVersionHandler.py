import sys

PYTHON_VERSION = sys.version_info[0]
#os.environ['PYSPARK_PYTHON'] = '/root/anaconda3/bin/python'

WRITE_OUTPUTS = True
LOGGING = True
HIGH_LOGGING = LOGGING and True

def print_(*args):
    import os, paths
    line = ''
    for ar in args:
        line += str(ar) + ' '
    line = line[:-1]+'\n'
    print(line[:-1])
    global WRITE_OUTPUTS
    if WRITE_OUTPUTS:        
        if paths.COMPUTERNAME == 'osldevptst02':
            outputFileName = paths.joinPath('outputs', 'output20.txt')
        else:
            outputFileName = paths.joinPath('outputs', 'output_local.txt')
        if os.path.isfile(outputFileName):
            open(outputFileName, 'a').write(line)  
        else:
            open(outputFileName, 'w').write(line)  
    
def print_logging(*args):
    if LOGGING: 
        line = ''
        for ar in args:
            line += str(ar) + ' '
        line = line[:-1]+'\n'
        print_(line[:-1])

def print_high_logging(*args):
    if LOGGING and HIGH_LOGGING: 
        line = ''
        for ar in args:
            line += str(ar) + ' '
        line = line[:-1]+'\n'
        print_(line[:-1])

def myXrange(i):
    if PYTHON_VERSION == 2:
        return xrange(i)
    else:
        return range(i)
        
def nowStr():
    from datetime import datetime
    return str(datetime.now())

def uniqueList(l): 
    return list(set(l))