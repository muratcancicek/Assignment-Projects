
def isMobile(m):
    import LumberjackConstants as L
    return L.KEY_TYPE in m.keys() and (m[L.KEY_TYPE] == L.KEY_TYPE_MOBILE_SITE or m[L.KEY_TYPE] == L.KEY_TYPE_MOBILE_DEVICE)

def isBotAgent(m):
    import BotUtil
    import LumberjackConstants as L
    return not isMobile(m) and L.KEY_AGENT in m and BotUtil.isBotAgent(m[L.KEY_AGENT])
a =0
def parse(input):
    import StringUtil, LumberjackConstants as L
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
    if (L.KEY_USER_ID in map):
        memberId = map[L.KEY_USER_ID]
    elif ((L.KEY_USER_ID_FROM_COOKIE) in map):
        if (',' in map[L.KEY_USER_ID_FROM_COOKIE]):
            values = map[L.KEY_USER_ID_FROM_COOKIE].split(',')
            if (len(values) == 2):
                memberId = values[1]
            else:
                memberId = '0'
        else:
            memberId = map[L.KEY_USER_ID_FROM_COOKIE]
    else:
        memberId = '0'
    if not memberId == '0':
        map[L.KEY_USER_ID_FOUND] = memberId
    map[L.KEY_TIMESTAMP] = str[0]
    return map

