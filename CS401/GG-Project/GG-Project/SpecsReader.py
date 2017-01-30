import urllib, json, sys, os
from paths import *

def getCategorySpecs(categoryCode, asString = False):
    url = "http://ap-api-java.pool.gittigidiyor.net:8080/gbay/categories/" + categoryCode + "/specs"
    response = urllib.urlopen(url)
    s = response.read()
    return s if asString else json.loads(s)

def saveSpecs(filename = specsFolder + 'raw_all_specs.bson'):
    f = open(filename, 'w')
    f.write('[\n')
    for code in codes[:-1]:
        f.write(getCategorySpecs(code, True))
        f.write(', \n')
    f.write(getCategorySpecs(codes[-1], True))
    f.write(' \n]')
    f.close()

def flattenSpecs(readingFileName =  specsFolder + 'raw_all_specs.bson', writingFileName =  specsFolder + 'all_specs.bson'):
    readingFile = open(readingFileName, "rU")
    writingFile = open(writingFileName, 'w')
    rawLines = readingFile.read().split('\n')
    newLineIndex = 0
    lineToWrite = rawLines[0]
    for index in range(1, len(rawLines)):
        rawLine = rawLines[index]
        if rawLine[0] in ['[', '{', ']']: 
            writingFile.write(lineToWrite + '\n')
            lineToWrite = rawLine
        else:
            lineToWrite = lineToWrite[:-3] + rawLine
    writingFile.write(']')

def getAllCategorySpecs(fileName =  specsFolder + 'all_specs.bson'):
    #dir = os.path.dirname(__file__)
    #print dir
    #fileName = os.path.join('generated', 'produced', 'all_specs.bson')
    #print fileName
    f = open(fileName, 'rb') 
    rawLines = f.read().decode('utf-8').replace('null', 'None').replace('true', 'True').replace('false', 'False')
    rawLines = eval(rawLines)
    specsDict = {}
    for line in rawLines:
        specsDict[line['data']['categoryCode']] = line['data']
    return specsDict


