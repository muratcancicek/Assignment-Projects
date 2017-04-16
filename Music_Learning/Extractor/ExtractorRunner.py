from paths import *
from SystemHelpers.PythonVersionHandler import *

def run(musicFile, featuresFile):
    print_(getFixedEncodingValue(musicFile), 'is being processed...', nowStr())
    #os.system('""')
    os.system('"' + extractorExe + ' "' + musicFile + '" "' + featuresFile + '"')
    #print_(featuresFile, 'has been saved successfully.')
    print_(' ')