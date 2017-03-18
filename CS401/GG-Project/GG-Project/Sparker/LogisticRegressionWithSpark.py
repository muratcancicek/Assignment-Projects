from .MlLibHelper import *

def runLogisticRegressionWithSpark(sc = None):
    if sc == None: sc = SparkContext()
    trainData = readCSVDataAsLabeledPoints(sc, trainUSPSFileName)
    testData = readCSVDataAsLabeledPoints(sc, testUSPSFileName)
    #trainData.foreach(print_)

    ## Build the model
    #model = LogisticRegressionWithLBFGS.train(trainData)

    ## Evaluating the model on testing data
    #evaluateModelOnData(model, testData)

    # Save and load model
    #saveLogisticRegressionSparkModel(sc, model)
    modelFileName = 'pythonLogisticRegressionWithLBFGSModel'
    sameModel = loadLogisticRegressionSparkModel(sc, modelFileName)
    
    print_(sameModel.weights)
    
    evaluateModelOnData(sameModel, testData)