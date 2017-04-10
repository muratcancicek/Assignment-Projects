from Extractor.ExtractorRunner import run as runExtractor 
from Tests.MusicTraverserTest import runtraverseMusicTest
from paths import *

def printSeparater():
    for n in range(3):
        print_('#' * 88)

def main():
    runtraverseMusicTest()

printSeparater()
print_('%s:' % nowStr(), 'Running on', COMPUTERNAME + '...')
main()
print_('%s:' % nowStr(), 'DONE')
printSeparater()

import sys
sys.exit() 