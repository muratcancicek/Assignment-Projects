from paths import *

def run(musicFile, featuresFile):
    print_(getFixedEncodingValue(musicFile), 'is being processed...')
    #os.system('""')
    os.system('"' + extractorExe + ' "' + musicFile + '" "' + featuresFile + '"')
    #print_(featuresFile, 'has been saved successfully.')
    print_(' ')