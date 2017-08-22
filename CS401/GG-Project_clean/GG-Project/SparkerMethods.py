l = []
def addPyFiles(sc, dr):
    import os, paths
    for filename in os.listdir(dr):
        #if filename in l: continue
        l.append(filename)
        p = paths.joinPath(dr, filename)
        if filename[-3:] == '.py':
            #print(p)
            sc.addPyFile(p) 
        #elif os.path.isdir(p):
        #    ##sc.addPyFile(p) 
        #    sc = addPyFiles(sc, p)
    return sc

def runSpark():
    import os
    import sys
    SPARK_HOME = os.environ['SPARK_HOME']

    # Add the PySpark\\py4j to the Python Path
    sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib"))
    sys.path.insert(0, os.path.join(SPARK_HOME, "python"))
    sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib", "py4j-0.10.4-src.zip"))

    import paths, pyspark, SparkLogFileHandler
    conf = pyspark.SparkConf()
    conf.set("spark.master", "spark://osldevptst02.host.gittigidiyor.net:7077")
    conf.set("spark.executor.memory", "12g")
    conf.set("spark.executor.instances", "2")
    sc = pyspark.SparkContext(conf=conf) 
    dr = paths.joinPath(paths.joinPath(paths.joinPath(paths.gitDir, 'CS401'), 'GG-Project_clean'), 'GG-Project')
    sc = addPyFiles(sc, dr)
    SparkLogFileHandler.setSparkContext(sc)

def run(): 
    runSpark() 
    import NewExtractorRunner
    NewExtractorRunner.runNewExtractionMethods()