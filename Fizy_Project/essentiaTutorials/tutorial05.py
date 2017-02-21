from essentia.standard import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paths import *

def savingYAMLMelBandsEnergiesMFCCsInFramesFromPool(fileName):
    loader = MonoLoader(filename = joinPath(mp3sFolder, fileName + '.mp3'))
    # and then we actually perform the loading:
    audio = loader()
    pool = essentia.Pool()
    w = Windowing(type = 'hann')
    spectrum = Spectrum()
    mfcc = MFCC()
    for frame in FrameGenerator(audio, frameSize=1024, hopSize=512, startFromZero=True):
        mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
        pool.add('lowlevel.mfcc', mfcc_coeffs)
        pool.add('lowlevel.mfcc_bands', mfcc_bands)

    plotPath = joinPath(plotsFolder, fileName)
    outputPath = joinPath(plotPath, 'mfcc.sig')
    output = YamlOutput(filename = outputPath) # use "format = 'json'" for JSON output
    outputPath = joinPath(plotPath, 'mfcc.json')
    output = YamlOutput(filename = outputPath, format = 'json') 
    output(pool)

    aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)

    print 'Original pool descriptor names:'
    print pool.descriptorNames()
    print
    print 'Aggregated pool descriptor names:'
    print aggrPool.descriptorNames()

    # and ouput those results in a file
    outputPath = joinPath(plotPath, 'mfccaggr.sig')
    YamlOutput(filename = outputPath)(aggrPool)
    outputPath = joinPath(plotPath, 'mfccaggr.json')
    YamlOutput(filename = outputPath, format = 'json')(aggrPool)
    
def runTutorial05():
    savingYAMLMelBandsEnergiesMFCCsInFramesFromPool('HotlineBling')
    savingYAMLMelBandsEnergiesMFCCsInFramesFromPool('adaSahilleri')