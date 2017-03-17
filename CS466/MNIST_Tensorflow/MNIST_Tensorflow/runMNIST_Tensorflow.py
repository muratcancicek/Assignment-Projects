from datetime import datetime
from PythonVersionHandler import *
from Main import main
import sys

def printSeparater():
    for n in range(3):
        print_('#' * 88)
        
def nowStr():
    return str(datetime.now())

printSeparater()
print_('%s:' % nowStr(), 'Running...')
main()
print_('%s:' % nowStr(), 'DONE')
printSeparater()

sys.exit() 
#   C:\Fast_STORAGE\tensorflowGPU0p12\Scripts\activate tensorflowGPU0p12