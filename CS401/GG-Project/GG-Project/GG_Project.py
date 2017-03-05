from FirstTermMethods import *
from SecondTermMethods import run as runSecondTermMethods
from datetime import datetime

def printSeparater():
    for n in range(3):
        print '#' * 88
def main(): 
    runSecondTermMethods()

printSeparater()
print '%s:' % str(datetime.now()), 'Running...'
main()
print '%s:' % str(datetime.now()), 'DONE'
printSeparater()

import sys
sys.exit() 