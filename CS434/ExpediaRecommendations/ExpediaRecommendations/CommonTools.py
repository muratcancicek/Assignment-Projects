import math
import average_precision as ap
from collections import defaultdict
import numpy as np 

DEFAULT_LABEL_INDEX = 0

###############################  predictions  #################################

def readPredictions(fileName):
    preds = pd.read_csv(fileName)
    predictions = []
    for p in preds['hotel_cluster']:
        p  = p.split()
        predictions.append([int(i) for i in p])
    return predictions

###############################  ACCURACY  ####################################

def getAccuracyCount(testSet, predictions, labelIndex = DEFAULT_LABEL_INDEX):
	accuracyCount = 0
	for x in range(len(testSet)):
		if isinstance(testSet[x], list):
		    if testSet[x][labelIndex] == predictions[x]:
		        accuracyCount += 1
		else:
		    if testSet[x] == predictions[x]:
		        accuracyCount += 1
	return accuracyCount
	
#################################  ERROR  #####################################

def getErrorCount(testSet, predictions, labelIndex = DEFAULT_LABEL_INDEX):
	errorCount = 0
	for x in range(len(testSet)):
		if isinstance(testSet[x], list):
		    if testSet[x][labelIndex] != predictions[x]:
		        errorCount += 1
		else:
		    if testSet[x] != predictions[x]:
		        errorCount += 1
	return errorCount

###############################  get actuals  #################################

def getActualHotelClusters(fileName): 
    t2 = pd.read_csv(fileName)
    t = t2['hotel_cluster'].tolist()
    actuals = [[l] for l in t]
    return actuals

###############################  ACCURACY  ####################################

def getAccuracyMAPK(actuals, predictions, k = 5):
    accuracy = ap.mapk(actuals, predictions, k)
    print 'Accuracy:', accuracy, '\n'

###############################  ACCURACY  ####################################

def getAccuracy(testSet, predictions, labelIndex = DEFAULT_LABEL_INDEX):
	accuracyCount = getAccuracyCount(testSet, predictions, labelIndex)
	return percentage(testSet, accuracyCount)

###############################  PERCENTAGE  ##################################

def percentage(dataset, count):
    return (count/float(len(dataset))) * 100

#############################  FORMATTING FLOATS  #############################

def removezeros(number):
    number = '%.15f' % number
    while len(number):
        if number[::-1][0] == '0':
            number = number[:-1]
        elif number[::-1][0] == '.':
            number = number[:-1]
            break
        else:
            break
    return number

############################  LIST TRANSPOSE  #################################

def transposeList(l):
    return map(list, zip(*l))

############################  my print  #######################################

def printSave(*args):
    string = ''
    if len(args) > 0: 
        string = str(args[0])
        if len(args) > 1: 
            for arg in args[1:]: string = string + ' ' + str(arg)
        print string
    with open("output.txt", "a") as myfile:
        myfile.write(string + '\n')

def save(*args):
    string = ''
    if len(args) > 0: 
        string = str(args[0])
        if len(args) > 1: 
            for arg in args[1:]: string = string + ' ' + str(arg)
    with open("output.txt", "a") as myfile:
        myfile.write(string + '\n')

############################  my print  #######################################

def valueCounter(column, fileName):
    values = set()
    counts = defaultdict(int)
    def helper(row):
        value = row[column]
        if value in values:
            counts[value] += 1
        else:
            counts[value] = 1
            values.add(value)
    iterateRows(helper, fileName)
    return counts

def iterateRows(function, fileName):
    print('Preparing to read ' + fileName + '...\n')
    f = open(fileName, "r")
    f.readline()
    total = 0
    while 1:
        line = f.readline().strip()
        total += 1
        if total % 250000 == 0: print('Read {} lines...'.format(total)) 
        if line == '': break
        function(line.split(","))
    print(fileName + ' has been read.\n')


def getDType():
    return {'date_time': str, 'site_name': np.int32, 'posa_continent': np.int32, 'user_location_country': np.int32,\
        'user_location_region': np.int32, 'user_location_city': np.int32, 'orig_destination_distance': float,\
        'user_id': np.int32, 'is_mobile': np.int32, 'is_package': np.int32, 'channel': np.int32, 'srch_ci': str, 'srch_co': str,\
        'srch_adults_cnt': np.int32, 'srch_children_cnt': np.int32, 'srch_rm_cnt': np.int32, 'srch_destination_id': np.int32,\
        'srch_destination_type_id': np.int32, 'hotel_continent': np.int32, 'hotel_country': np.int32, 'hotel_market': np.int32,\
        'is_booking': np.int32, 'cnt': long, 'hotel_cluster': np.int32}

def getColumnNames():
    return ['date_time', 'site_name', 'posa_continent', 'user_location_country', 'user_location_region', 'user_location_city',\
        'orig_destination_distance', 'user_id', 'is_mobile', 'is_package', 'channel', 'srch_ci', 'srch_co', 'srch_adults_cnt',\
        'srch_children_cnt', 'srch_rm_cnt', 'srch_destination_id', 'srch_destination_type_id', 'hotel_continent', 'hotel_country',\
        'hotel_market', 'is_booking', 'cnt', 'hotel_cluster']

def getColumnDict():
    dictionary = {}
    columnNames = getColumnNames()
    for columnIndex in range(len(columnNames)):
        dictionary[columnNames[columnIndex]] = columnIndex
    return dictionary

def getNewNames():
    return ['date_time', 'user_location_city', 'srch_destination_id',  \
                'user_id', 'hotel_continent', 'hotel_country', 'hotel_market', 'hotel_cluster']
def writeNames(fileName):
    file = open(fileName, "a")
    columnNames = getColumnDict()
    newNames = ['date_time', 'user_location_city', 'orig_destination_distance', 'srch_destination_id',  \
                'user_id', 'hotel_continent', 'hotel_country', 'hotel_market', 'hotel_cluster']
    for name in newNames[:-1]:
        file.write(name + ',')
    file.write(newNames[-1] + '\n')
    file.close()
    return columnNames, newNames

c = -1
def writeNewTrain(fromFile, newFile, testFile):
    columnNames, newNames = writeNames(newFile)
    writeNames(testFile)
    indexOf = lambda name: columnNames[name]
    def writeableRow(row):
        line = row[indexOf(newNames[0])][:7]
        for name in newNames[1:]:
            line = line + ',' + row[indexOf(name)]
        line = line + '\n'
        return line
    def writeTrain(row):
        with open(newFile, "a") as myfile:
            myfile.write(writeableRow(row))
    def writeTest(row):
        with open(testFile, "a") as myfile:
            myfile.write(writeableRow(row))
    
    trainClusterCounters = defaultdict(int)
    def controlTrain(cluster, row):
        if cluster in trainClusterCounters.keys():
            if trainClusterCounters[cluster] < 18835:
               trainClusterCounters[cluster] += 1
               writeTrain(row)
        else:
            trainClusterCounters[cluster] = 1
            print 'new Train'
            writeTrain(row)

    testClusterCounters = defaultdict(int)
    def controlTest(cluster, row):
        if cluster in testClusterCounters.keys():
            if testClusterCounters[cluster] < 2528:
               testClusterCounters[cluster] += 1
               writeTest(row)
        else:
            testClusterCounters[cluster] = 1
            print 'new Test'
            writeTest(row)

    def filterRows(row):
        global c
        c += 1
        if c % 3 != 0 or row[columnNames['orig_destination_distance']] == '': return None
        date = row[columnNames['date_time']]
        year, month = int(date[:4]), int(date[5:7])
        cluster = row[columnNames['hotel_cluster']]
        if (year == 2013) or ((year == 2014) and (month < 8)):
            controlTrain(cluster, row)
        else:
            controlTest(cluster, row)
    iterateRows(filterRows, fromFile)