from datetime import datetime
from PythonVersionHandler import *
from Main import main
import sys

def printSeparater():
    for n in range(4):
        print_('#' * 88)
        
def nowStr():
    return str(datetime.now())
total = len(sys.argv)
if total != 3:
    print_('wrong argument count')
    sys.exit() 
cmdargs =sys.argv
printSeparater()
print_('%s:' % nowStr(), 'Running...')
main(cmdargs)
print_('%s:' % nowStr(), 'DONE')
printSeparater()

sys.exit() 