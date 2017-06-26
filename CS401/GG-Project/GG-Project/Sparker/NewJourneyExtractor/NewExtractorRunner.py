from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from LogProcesser.scalaToPython.python_codes.LumberjackParser import *

aLog = '1475748081404	_bot=0&_ip=990d2eacf79a5470c088abab769b43793bc08fb893b95b67b26ef0caf3e1da61&agent=Mozilla%2F5.0+%28Windows+NT+6.1%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F44.0.2403.157+Safari%2F537.36&format=1%2C2%2C3%2C4&ids=240889665%2C238192843%2C243970265%2C242362312%2C221822513%2C242762098%2C242763405%2C242773118%2C242783582%2C205957817%2C242772952%2C242784936%2C242784219%2C192488364%2C177536620%2C177536618%2C222616340%2C178036211%2C243216434%2C206077575%2C192490709%2C192490706%2C177536623%2C177552549%2C223065773%2C242782937%2C221850395%2C242768370%2C242768345%2C177536619%2C242778750%2C221850723%2C192500433%2C192491290%2C242778737%2C211014665%2C222620920%2C242783759%2C199526690%2C194882196%2C242771775%2C242779014%2C195716868%2C243671990%2C242313528%2C242304253%2C243257684%2C211014830%2C226194674%2C238538743%2C238538739%2C243808776%2C238053534%2C241375396%2C181083138%2C241454478%2C241440970%2C240201754%2C240335308%2C241235918&keyword=nokia+lumia+1020&module=search&orderBy=wbm&pageNum=1&referer=https%3A%2F%2Fwww.google.com.tr%2F&resultType=catalog&sid=2drgtm84o68as2d67pvba3cht2&source=zf&totfound=308'

def getValueOf(key, log):
    begin = log.find(key + '=')
    if begin == -1:
        #print_('Key not found:', key)
        raise KeyError
    else:
        begin = begin + len(key) + 1
    end = log[begin:].find('&')
    end = begin + (end if end != -1 else len(log))
    return log[begin:end]

relevantModules = [KEY_MODULE_SEARCH, KEY_MODULE_ITEM, KEY_MODULE_CART, KEY_MODULE_PAYMENT]
def isRelevantModule(log):
    try:
        return getValueOf(KEY_MODULE, log) in relevantModules
    except KeyError:
        return False

def isBot(log):
    m = {}
    try:
        m[KEY_AGENT] = getValueOf(KEY_AGENT, log)
    except KeyError:
        pass
    try:
        m[KEY_TYPE] = getValueOf(KEY_TYPE, log)
    except KeyError:
        pass
    try:
        #isb = 
        #if isb:
        #    print_(69, getValueOf(KEY_BOT, log))#orisBotAgent(m) 
        return  getValueOf(KEY_BOT, log) != '0'
    except KeyError:
        return False

def isRelevant(log):
    return isRelevantModule(log) and not isBot(log)

def runNewExtractionMethods():
    logsFile = joinPath(clickstreamFolder, 'part-r-00000')
    logs = readLogs(sc_(), logsFile)
    print_(logs.count())
    #logs = logs.filter(isBot)
    #print_(logs.count())
    logs = logs.filter(isRelevant)
    print_(logs.count())