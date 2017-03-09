import sys
import paths

class OutputLogger(object):
    def __init__(self, outputFolder, outputFileName = 'output.txt'):
        self.terminal = sys.stdout
        outputFileName = paths.joinPath(outputFolder, outputFileName)
        self.log = open(outputFileName, 'a') #open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    