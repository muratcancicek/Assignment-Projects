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
    s = JSONEncoder().encode(bson)
    if decoding != 'None': s = s.decode(decoding)
    #s =json.dumps(bson).decode('unicode-escape')
    if p: print s
    return s 

def evalBson(fileName, decoding = 'utf-8'):
    f = open(fileName, 'rb')
    rawLines = f.read()
    if decoding != 'None': rawLines.decode(decoding)
    rawLines = rawLines.replace('null', 'None').replace('true', 'True').replace('false', 'False')
    return eval(rawLines)

def fixQuotes(text):
    index = 0
    while index < len(text):
        index = text.find('\"', index)
        if index == -1:
            break
        text = text[:index] + '\\' + text[index:] 
        index += 2
    return text
#text.encode(decoding) if decoding != 'None' else 
def writeToBson(bson, fileName,  printing = False, printText = False, decoding = 'utf-8'): 
    f = open(fileName, 'wb')
    text = ('{\n' if type(bson) is dict else '[\n')
    if type(bson) is dict:
        for k, v in bson.items():
            line = ('\"' + fixQuotes(k) + '\": ' + printBson(v, printing, 'None') + ',\n')
            if printing: print line
            text += line
    else:
        for v in bson:
            text += (printBson(v, printing, decoding) + ',\n')
    text = text[:-2] + ('\n}' if type(bson) is dict else '\n]')
    if printText: print text
    f.write(text.encode('utf8')) 
    f.close()