from .MLlibTests.MlLibHelper import *
from .MLlibTests import LogisticRegressionFromCS434_HW2

def countModule(sc, module = 'item'):
    if sc == None: sc = SparkContext() 
    fileName = joinPath(clickstreamFolder, 'part-r-00000')
    lines = sc.textFile(fileName)
    #lines = sc.textFile('D:\\OneDrive\\Projects\\Assignment-Projects\\CS401\\GG-Project\\GG-Project\\data\\ranking\\clickstream\\part-r-00000')
    lines = lines.map(lambda l: LumberjackParser.parse(l))#l.split('\t'))print(x)toLocalIterator()
    lines = lines.filter(lambda l: l['module'] == module)
    #lines.foreach(print_)
    print(lines.count(), module, 'found.') 

def testToTrainFM_parallel_sgd(sc = None):
    trainData = readCSVDataAsSparseVectors(sc, trainUSPSFileName)
    testData = readCSVDataAsSparseVectors(sc, testUSPSFileName)
        
    optimalW = fm_parallel_sgd.trainFM_parallel_sgd(sc, trainData, iterations=1, evalTraining=False)
    evaluateFM_SGD(testData, optimalW)
    
    optimalW = fm_parallel_sgd.trainFM_sgd(trainData, iterations=1)
    evaluateFM_SGD(testData, optimalW)

def PySparkTutorial1Test1(sc = None):
    if sc == None: sc = SparkContext()
    lines = sc.textFile('D:\\OneDrive\\Projects\\Assignment-Projects\\CS401\\GG-Project\\GG-Project\\data\\productToPoint\\common\\ProductVector.csv')
    lines = lines.map(lambda line: [np.float64(v) for v in line.split(",")])
    lines = lines.map(lambda line: {'features':line[:-7], 'label': line[-1]})
    #lines.foreach(print)
    w = trainFM_parallel_sgd(sc, lines, iterations=5)
    print_(w)
#test()
