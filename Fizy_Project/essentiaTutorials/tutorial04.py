from essentia.standard import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paths import *

def ComputingMelBandsEnergiesMFCCsInFramesFromPool(fileName):
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
    fig = plt.figure()
    # and plot
    plt.imshow(pool['lowlevel.mfcc_bands'].T, aspect = 'auto', origin='lower', interpolation='none')
    plt.title("Mel band spectral energies in frames")
    plt.savefig(joinPath(plotPath, 'MelBandSpectralEnergiesInFramesFromPool.png'))

    plt.imshow(pool['lowlevel.mfcc'].T[1:,:], aspect='auto', origin='lower', interpolation='none')
    plt.title("MFCCs in frames")
    plt.savefig(joinPath(plotPath,'MFCCsInFramesFromPool.png'))

    plt.close(fig)
    
def runTutorial04():
    ComputingMelBandsEnergiesMFCCsInFramesFromPool('HotlineBling')
    ComputingMelBandsEnergiesMFCCsInFramesFromPool('adaSahilleri')