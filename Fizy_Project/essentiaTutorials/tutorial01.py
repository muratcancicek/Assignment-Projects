import essentia.standard as ess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paths import *

def plotSecondSecond(fileName):
    # we start by instantiating the audio loader:
    loader = ess.MonoLoader(filename= joinPath(mp3sFolder, fileName + '.mp3'))
    # and then we actually perform the loading:
    audio = loader()
    # pylab contains the plot() function, as well as figure, etc... (same names as Matlab)
    fig = plt.figure()
    plt.rcParams['figure.figsize'] = (15, 6) # set plot sizes to something larger than default

    plt.plot(audio[1*44100:2*44100])
    plt.title('This is how the 2nd second of ' + fileName + ' looks like:')
    plt.savefig(joinPath(plotsFolder, joinPath(fileName, '2ndSecondOf' + fileName + '.png')))
    plt.close(fig)
    
def runTutorial01():
    plotSecondSecond('HotlineBling')
    plotSecondSecond('adaSahilleri')