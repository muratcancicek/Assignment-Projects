from paths import *
from MainSrc.PythonVersionHandler import *
from MainSrc.SecondTermMethods import run as runSecondTermMethods
from MainSrc.FirstTermMethods import run as runFirstTermMethods
from MainSrc.SparkerMethods import run as runSparkerMethods

def printSeparater():
    for n in range(3):
        print_('#' * 88)

def main():
    print_()
    #runSparkerMethods()

printSeparater()
print_('%s:' % nowStr(), 'Running on', os.getenv('COMPUTERNAME') + '...')
main()
print_('%s:' % nowStr(), 'DONE')
printSeparater()

import sys
sys.exit() 