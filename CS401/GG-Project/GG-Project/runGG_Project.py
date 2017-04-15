from paths import *
from MainSrc.PythonVersionHandler import *
#from MainSrc.SecondTermMethods import run as runSecondTermMethods
#from MainSrc.FirstTermMethods import run as runFirstTermMethods
from MainSrc.SparkerMethods import run as runSparkerMethods

def printSeparater():
    for n in range(3):
        print_('#' * 88)

def main():
    printSeparater()
    print_('%s:' % nowStr(), 'Running on', os.getenv('COMPUTERNAME') + '...')

    runSparkerMethods()

    print_('%s:' % nowStr(), 'DONE')
    printSeparater()

    sys.exit() 

if __name__ == "__main__":
    main()