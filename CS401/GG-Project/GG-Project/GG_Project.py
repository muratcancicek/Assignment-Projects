from FirstTermMethods import *
from SecondTermMethods import run as runSecondTermMethods

def printSeparater():
    for n in range(3):
        print '#' * 88
def main(): 
    runSecondTermMethods()

printSeparater()
print '%s:' % nowStr(), 'Running...'
main()
print '%s:' % nowStr(), 'DONE'
printSeparater()

import sys
sys.exit() 