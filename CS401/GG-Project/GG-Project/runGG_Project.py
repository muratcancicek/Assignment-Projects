from paths import *
from MainSrc.PythonVersionHandler import *
#from MainSrc.SecondTermMethods import run as runSecondTermMethods
#from MainSrc.FirstTermMethods import run as runFirstTermMethods
from MainSrc.SparkerMethods import run as runSparkerMethods
from DeepLearningToRank.DeepLearningToRankTest import runTests

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

    if  COMPUTERNAME != 'UCSC:citrisdense':
        sys.exit() 

if __name__ == "__main__":
    main()