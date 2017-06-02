from PythonVersionHandler import *
from AnalyzingTester import runTests
from paths import *

def printSeparater():
    for n in range(3):
        print_('#' * 88)
        
def main(method = None):
    printSeparater()
    print_('%s:' % nowStr(), 'Running on', COMPUTERNAME + '...')
    
    if method == None:
        runTests()
    else:
        method()

    print_('%s:' % nowStr(), 'DONE')
    printSeparater()

    if COMPUTERNAME == 'MSI' or COMPUTERNAME == 'LM-IST-00UBFVH8':
        sys.exit() 

if __name__ == "__main__":
    main()