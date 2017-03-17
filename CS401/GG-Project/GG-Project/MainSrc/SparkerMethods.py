from Sparker.LogisticRegressionFromCS434_HW2 import main as hw2Main
from Sparker.LogisticRegressionWithSpark import runLogisticRegressionWithSpark
from Sparker.PySparkTutorial1 import *

def runSparkerTests():
    countModule()
    hw2Main()

def run(): 
    #runSparkerTests()
    runLogisticRegressionWithSpark()