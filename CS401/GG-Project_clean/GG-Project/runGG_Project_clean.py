import os
import sys
SPARK_HOME = os.environ['SPARK_HOME']

# Add the PySpark\\py4j to the Python Path
sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib"))
sys.path.insert(0, os.path.join(SPARK_HOME, "python"))

def printSeparater():
    import PythonVersionHandler
    for n in range(3):
        PythonVersionHandler.print_('#' * 88)
        
def main(method = None, kill = True):
    printSeparater()
    import PythonVersionHandler, paths
    PythonVersionHandler.print_('%s:' % PythonVersionHandler.nowStr(), 'Running on', paths.COMPUTERNAME)

    if method == None:
        import SparkerMethods
        SparkerMethods.run()
    else:
        method()

    PythonVersionHandler.print_('%s:' % PythonVersionHandler.nowStr(), 'DONE')
    printSeparater()

    if  COMPUTERNAME != 'UCSC:citrisdense' and kill:
        import sys
        sys.exit() 

if __name__ == "__main__":
    main()
