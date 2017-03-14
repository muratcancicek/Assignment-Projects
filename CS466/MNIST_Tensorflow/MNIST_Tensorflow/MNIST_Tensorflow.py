from datetime import datetime
from VersionHandler import *
from Main import main
import sys

def printSeparater():
    for n in range(3):
        prnt('#' * 88)
        
def nowStr():
    return str(datetime.now())

printSeparater()
prnt('%s:' % nowStr(), 'Running...')
main()
prnt('%s:' % nowStr(), 'DONE')
printSeparater()

sys.exit() 