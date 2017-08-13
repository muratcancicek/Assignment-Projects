from LumberjackConstants import * 
import StringUtil
import BotUtil

def isMobile(m):
    return KEY_TYPE in m.keys() and (m[KEY_TYPE] == KEY_TYPE_MOBILE_SITE or m[KEY_TYPE] == KEY_TYPE_MOBILE_DEVICE)

def isBotAgent(m):
    return not isMobile(m) and KEY_AGENT in m and BotUtil.isBotAgent(m[KEY_AGENT])
a =0
def parse(input):
    str = input[:-1].split('\t')
    #global a
    #a += 1
    #print(a)
    map = {}
    # time?
    if len(str) < 2:
        return {}
    pairList = str[1].split('&')
    for p in pairList:
        pair = p.split('=')
        if (len(pair) > 1):
            #map[pair[0]] = pair[1].decode('utf-8')
            #encoded = encoded.replace('%C3%83%C2%87'.encode('utf-8'), '%C3%87') # c
            map[pair[0]] = StringUtil.getFixedEncodingValue(pair[1])#.encode('utf-8')
            #keyword = URLDecoder.decode(StringUtil.getFixedEncodingValue(pair[1])), 'utf-8')
            #(pair(0) -> keyword)
        else:
            map[len(map.keys())] = pair[0]

    memberId = '0'
    if (KEY_USER_ID in map):
        memberId = map[KEY_USER_ID]
    elif ((KEY_USER_ID_FROM_COOKIE) in map):
        if (',' in map[KEY_USER_ID_FROM_COOKIE]):
            values = map[KEY_USER_ID_FROM_COOKIE].split(',')
            if (len(values) == 2):
                memberId = values[1]
            else:
                memberId = '0'
        else:
            memberId = map[KEY_USER_ID_FROM_COOKIE]
    else:
        memberId = '0'
    if not memberId == '0':
        map[KEY_USER_ID_FOUND] = memberId
    map[KEY_TIMESTAMP] = str[0]
    return map

