from Sparker.LogisticRegressionImpOnSpark import runLogisticRegressionImplementationOnSpark
from Sparker.LogisticRegressionWithSpark import runLogisticRegressionWithSpark
from Sparker.HousingTutorialWithFM import runHousingTutorialWithFM
from Sparker.LogisticRegressionFromCS434_HW2 import main as hw2Main
from Sparker.PySparkTutorial1 import *
from Sparker.MlLibHelper import *

def runSparkerTests(sc):
    countModule(sc)
    hw2Main()
    runLogisticRegressionWithSpark(sc)
    testToTrainFM_parallel_sgd(sc)
    runLogisticRegressionImplementationOnSpark(sc)

def run(): 
    sc = SparkContext()
    runHousingTutorialWithFM(sc)
    #runSparkerTests(sc)
    

#   sshpass -p 'eBay@2017' ssh miek@127.0.0.1 
#   sshpass -p 'eBay@2017' ssh miek@10.200.133.227
#   sshpass -p 3022 'eBay@2017' ssh miek@10.200.133.227
#   shh -p 22 miek@10.200.133.227   
#   10.200.133.227:5900