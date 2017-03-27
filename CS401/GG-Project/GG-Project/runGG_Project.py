from MainSrc.SecondTermMethods import run as runSecondTermMethods
from MainSrc.FirstTermMethods import run as runFirstTermMethods
from MainSrc.SparkerMethods import run as runSparkerMethods
from MainSrc.PythonVersionHandler import *

def printSeparater():
    for n in range(3):
        print_('#' * 88)

def main(): 
    runSparkerMethods()

printSeparater()
print_('%s:' % nowStr(), 'Running on', os.getenv('COMPUTERNAME') + '...')
main()
print_('%s:' % nowStr(), 'DONE')
printSeparater()

import sys
sys.exit() 