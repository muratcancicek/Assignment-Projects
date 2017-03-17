import sys

PYTHON_VERSION = sys.version_info[0]

def print_(*args):
        line = ''
        for ar in args:
            line += str(ar) + ' '
        print(line)
    #if PYTHON_VERSION == 2:
    #else:
    
def myXrange(i):
    if PYTHON_VERSION == 2:
        return xrange(id)
    else:
        range(id)
