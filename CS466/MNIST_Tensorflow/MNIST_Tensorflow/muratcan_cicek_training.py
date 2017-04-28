#   
#   By Muratcan Cicek,  S004233, Computer Science at Ozyegin University
#   

from datetime import datetime
from PythonVersionHandler import *
from Main import main
import sys

def printSeparater():
    for n in range(4):
        print_('#' * 88)
        
def nowStr():
    return str(datetime.now())
def run():
    printSeparater()
    print_('%s:' % nowStr(), 'Running...')
    main()
    print_('%s:' % nowStr(), 'DONE')
    printSeparater()

    sys.exit() 
run()