from MainSrc.PythonVersionHandler import *
from bson import json_util, ObjectId
from MainSrc.Printing import *
import json, re

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return bytes(o)
        return json.JSONEncoder.default(self, o)

def printJson(json, p = True, decoding = 'unicode-escape'):
    s = JSONEncoder()
    if decoding != 'None': s = s.encode(decoding)
    #s =json.dumps(json).decode('unicode-escape')
    if p: print_(s)
    return s 

def fixQuotes(text):
    if type(text) is bool or text == None:
        text = bytes(text) 
    #elif type(text) is unicode:
    #    return text.encode('utf-8')
    index = 0
    while index < len(text):
        index = text.find('\"', index)
        if index == -1:
            break
        if index != 0:
           if text[index-1] != '\\':
                text = text[:index] + '\\' + text[index:] 
        else:
            text = text[:index] + '\\' + text[index:] 
        index += 2
    return text

def jsonToString(json, printing = True, decoding = 'unicode-escape', separator = ' ', lmbda = lambda k: 'zzz' if k in ['title', 'subTitle'] else k, sort = True, deep = 0):
    if type(json) == bytes:
        v = fixQuotes(json.decode('utf8'))
        return '\"' + v + '\"'
    if type(json) == str:
        return '\"' + fixQuotes(json) + '\"'
    text = ''
    if type(json) is dict:
        text = '{' + separator
        keys = json.keys()
        for k in keys:
            json[k] = jsonToString(json[k], False, decoding, ' ', sort = sort, deep = deep+1)
        keys.sort(key=lmbda)
        for k in keys:
            strK = '' 
            strV = '' 
            if type(json[k]) is str:
                #print('I am an unicode!', json[k]) 
                strV = json[k].encode('utf-8')
            else:
                strV = json[k] 
            if type(k) is bytes:
                strK = fixQuotes(k)
            elif type(k) is str:
                strK = k.encode('utf-8')
            else:
                strK = bytes(k)
            line = ('\"' +  strK.decode('utf-8') + '\": ' + strV.decode('utf-8') + ',' + separator)
            text += line
        text = (text[:-2] if len(json) > 0 else text) + separator + '}'
    elif type(json) is list:
        if deep == 0 or (deep > 0 and sort):
            json.sort()
        text = '[' + separator
        for v in json: 
            text += jsonToString(v, False, decoding, sort = sort, deep = deep+1) + ',' + separator
        text = (text[:-2] if len(json) > 0 else text) + separator + ']'
    elif json is None:
        text += 'null'
    elif type(json) is bool:
        text += 'true' if json else 'false'
    else:
        text += bytes(json)
    if printing: print_(text)
    return text

def evalJson(fileName, printing = True):
    f = open(fileName + '.json', 'rU')
    rawLines = f.read().replace('null', 'None').replace('true', 'True').replace('false', 'False')
    data = eval(rawLines)
    if printing:
        print_(fileName + '.json has been read successfully.')
    return data

def writeToJson(json, fileName,  printing = False, printText = False, decoding = 'utf-8', sort = True, printLog = True): 
    f = open(fileName + '.json', 'wb')
    jsonString = jsonToString(json, printing, decoding, u'\n', sort = sort).encode(decoding)
    f.write(jsonString) 
    if printLog:
        print_(fileName + '.json has been written successfully.')
    f.close() 

def appendToJson(data, fileName,  printing = False, printText = False, decoding = 'utf-8', sort = True, printLog = True): 
    f = open(fileName + '.json', 'a')
    jsonString = json.dumps(data)
    f.write(jsonString) 
    if printLog:
        print_(fileName + '.json has been written successfully.')
    f.close() 

