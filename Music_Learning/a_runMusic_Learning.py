from FeatureProcesser.FeatureExtractor import extractFeatures
from paths import *

def printSeparater():
    for n in range(3):
        print_('#' * 88)

def main():
    extractFeatures()

printSeparater()
print_('%s:' % nowStr(), 'Running on', COMPUTERNAME + '...')
main()
print_('%s:' % nowStr(), 'DONE')
printSeparater()

import sys
sys.exit() 