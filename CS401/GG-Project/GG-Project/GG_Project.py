import sys
from FirstTermMethods import *
from SecondTermMethods import run as runSecondTermMethods

def printSeparater():
    for n in range(3):
        print '#' * 88
def main(): 
    runSecondTermMethods()

printSeparater()
print 'Running...'
main()
print 'DONE'
printSeparater()

sys.exit() 