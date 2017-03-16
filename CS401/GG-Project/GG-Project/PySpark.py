import os
import sys
import LogProcesser.scalaToPython.python_codes.LumberjackParser as LumberjackParser
SPARK_HOME = os.environ['SPARK_HOME']

# Add the PySpark\\py4j to the Python Path
sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib"))
sys.path.insert(0, os.path.join(SPARK_HOME, "python"))

from pyspark import SparkContext 
def wordCount():
    sc=SparkContext() 
    lines = sc.textFile('D:\\OneDrive\\Projects\\Assignment-Projects\\CS401\\GG-Project\\GG-Project\\data\\ranking\\clickstream\\part-r-00000')
    lines = lines.map(lambda l: LumberjackParser.parse(l))#l.split('\t'))print(x)toLocalIterator()
    lines.foreach(print)
    #print('tan muratcan', lines.top(1))
wordCount()