from paths import COMPUTERNAME

import os
import sys
SPARK_HOME = os.environ['SPARK_HOME']

# Add the PySpark\\py4j to the Python Path
sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib"))
sys.path.insert(0, os.path.join(SPARK_HOME, "python"))
import pyspark as ps


from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext, SparkConf
from py4j.protocol import Py4JJavaError
from pyspark.mllib.util import MLUtils
from pyspark.storagelevel import *
import pyspark.mllib.linalg
from pyspark.rdd import RDD, PipelinedRDD
from pyspark.mllib.feature import Normalizer
from py4j.protocol import Py4JJavaError
import LogProcesser.scalaToPython.python_codes.LumberjackParser as LumberjackParser

