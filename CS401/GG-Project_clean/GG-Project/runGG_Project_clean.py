
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
        SparkerMethods.run(setMaster = False)
    else:
        method()

    PythonVersionHandler.print_('%s:' % PythonVersionHandler.nowStr(), 'DONE')
    printSeparater()

    if  paths.COMPUTERNAME != 'UCSC:citrisdense' and kill:
        import sys
        sys.exit() 

if __name__ == "__main__":
    main()
