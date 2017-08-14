from paths import *
from PythonVersionHandler import *
#from SecondTermMethods import run as runSecondTermMethods
#from FirstTermMethods import run as runFirstTermMethods
#from DeepLearningToRank.DeepLearningToRankTest import runTests

def printSeparater():
    import PythonVersionHandler
    for n in range(3):
        PythonVersionHandler.print_('#' * 88)
        
def main(method = None, kill = True):
    printSeparater()
    import PythonVersionHandler, paths
    PythonVersionHandler.print_('%s:' % PythonVersionHandler.nowStr(), 'Running on', paths.COMPUTERNAME + '...')

    if method == None:
        import SparkerMethods
        SparkerMethods.run()
    else:
        method()

    PythonVersionHandler.print_('%s:' % PythonVersionHandler.nowStr(), 'DONE')
    printSeparater()

    if  COMPUTERNAME != 'UCSC:citrisdense' and kill:
        import sys
        sys.exit() 

if __name__ == "__main__":
    main()