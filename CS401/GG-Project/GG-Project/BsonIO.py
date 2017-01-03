import json, re
from bson import json_util, ObjectId

def readBson(filename):
    with open(filename, "rU") as f:
        # read the entire input; in a real application,
        # you would want to read a chunk at a time
        bsondata = f.read()

        # convert the TenGen JSON to Strict JSON
        # here, I just convert the ObjectId and Date structures,
        # but it's easy to extend to cover all structures listed at
        # http://www.mongodb.org/display/DOCS/Mongo+Extended+JSON
        jsondata = re.sub(r'ObjectId\s*\(\s*\"(\S+)\"\s*\)',
                          r'{"$oid": "\1"}',
                          bsondata.replace('\n', ' ')[3:])
        jsondata = re.sub(r'Date\s*\(\s*(\S+)\s*\)',
                          r'{"$date": \1}',
                          jsondata)

        # now we can parse this as JSON, and use MongoDB's object_hook
        # function to get rich Python data structures inside a dictionary
        data = json.loads(jsondata, object_hook=json_util.object_hook)
        return data
        # just print the output for demonstration, along with the type
        #print(data["elapsedTime"])
        #print(type(data))

        # serialise to JSON and print
        #print(json_util.dumps(data)).decode('utf-8')

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def printBson(bson, p = True, decoding = 'unicode-escape'):
    s = JSONEncoder()
    if decoding != 'None': s = s.encode(decoding)
    #s =json.dumps(bson).decode('unicode-escape')
    if p: print s
    return s 

def bsonToString(bson, printing = True, decoding = 'unicode-escape', separator = ' ', lmbda = lambda k: 'zzz' if k in ['title', 'subTitle'] else k, sort = True, deep = 0):
    if type(bson) == str:
        v = fixQuotes(bson.decode('utf8'))
        return '\"' + v + '\"'
    if type(bson) == unicode:
        return '\"' + fixQuotes(bson) + '\"'
    text = ''
    if type(bson) is dict:
        text = '{' + separator
        keys = bson.keys()
        for k in keys:
            bson[k] = bsonToString(bson[k], False, decoding, ' ', sort = sort, deep = deep+1)
        keys.sort(key=lmbda)
        for k in keys:
            strK = '' 
            strV = '' 
            if type(bson[k]) is unicode:
                #print('I am an unicode!', bson[k]) 
                strV = bson[k].encode('utf-8')
            else:
                strV = bson[k] 
            if type(k) is str:
                strK = fixQuotes(k)
            elif type(k) is unicode:
                strK = k.encode('utf-8')
            else:
                strK = str(k)
            line = ('\"' +  strK.decode('utf-8') + '\": ' + strV.decode('utf-8') + ',' + separator)
            text += line
        text = (text[:-2] if len(bson) > 0 else text) + separator + '}'
    elif type(bson) is list:
        if deep == 0 or (deep > 0 and sort):
            bson.sort()
        text = '[' + separator
        for v in bson: 
            text += bsonToString(v, False, decoding, sort = sort, deep = deep+1) + ',' + separator
        text = (text[:-2] if len(bson) > 0 else text) + separator + ']'
    elif bson is None:
        text += 'null'
    elif type(bson) is bool:
        text += 'true' if bson else 'false'
    else:
        text += str(bson)
    if printing: print text
    return text

def evalBson(fileName):
    f = open(fileName, 'rU')
    rawLines = f.read().replace('null', 'None').replace('true', 'True').replace('false', 'False')
    return eval(rawLines)

def fixQuotes(text):
    if type(text) is bool or text == None:
        text = str(text) 
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

def writeToBson(bson, fileName,  printing = False, printText = False, decoding = 'utf-8', sort = True): 
    f = open(fileName, 'wb')
    bsonString = bsonToString(bson, printing, decoding, u'\n', sort = sort).encode(decoding)
    f.write(bsonString) 
    f.close() 