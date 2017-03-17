from datetime import datetime
import time
import sys

PYTHON_VERSION = sys.version_info[0]

def print_(*args):
        line = ''
        for ar in args:
            line += str(ar) + ' '
        print(line)
    #if PYTHON_VERSION == 3:
    #    print
    ##else:
    
def myXrange(i):
    if PYTHON_VERSION == 2:
        return xrange(id)
    else:
        range(id)
        
def nowStr():
    return str(datetime.now())