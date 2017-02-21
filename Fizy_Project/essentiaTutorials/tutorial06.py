import essentia
from essentia.streaming import *
from paths import *

def streaming(fileName):
    loader = MonoLoader(filename = joinPath(mp3sFolder, fileName + '.mp3'))
    frameCutter = FrameCutter(frameSize = 1024, hopSize = 512)
    w = Windowing(type = 'hann')
    spec = Spectrum()
    mfcc = MFCC()

    loader.audio >> frameCutter.signal
    frameCutter.frame >> w.frame >> spec.frame
    spec.spectrum >> mfcc.spectrum

    pool = essentia.Pool()

    mfcc.bands >> None
    mfcc.mfcc >> (pool, 'lowlevel.mfcc')
    essentia.run(loader)
    
    plotPath = joinPath(plotsFolder, fileName)
    outputPath = joinPath(plotPath, 'mfccframes.txt')
    fileout = FileOutput(filename = outputPath)
    mfcc.mfcc >> fileout

    essentia.reset(loader)
    essentia.run(loader)

    print 'Pool contains %d frames of MFCCs' % len(pool['lowlevel.mfcc'])
    

def runTutorial06():
    streaming('HotlineBling')
    #streaming('adaSahilleri')