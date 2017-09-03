
def printSeparater():
    import PythonVersionHandler
    for n in range(3):
        PythonVersionHandler.print_('#' * 88)
        
def runOnJupyter(method = None, setMaster = False):
    printSeparater()
    import PythonVersionHandler, paths, SparkLogFileHandler
    PythonVersionHandler.print_('%s:' % PythonVersionHandler.nowStr(), 'Running on', paths.COMPUTERNAME)

    if SparkLogFileHandler.sc_() == None:
        import SparkerMethods
        SparkerMethods.runSpark(setMaster = setMaster)

    if method == None:
        import NewExtractorRunner
        NewExtractorRunner.runNewExtractionMethodsOnJupyter()
    else:
        method()

    PythonVersionHandler.print_('%s:' % PythonVersionHandler.nowStr(), 'DONE')
    printSeparater()