from essentia.standard import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paths import *

def ComputingMelBandsEnergiesMFCCsInFrames(fileName):
    loader = MonoLoader(filename = joinPath(mp3sFolder, fileName + '.mp3'))
    # and then we actually perform the loading:
    audio = loader()
    mfccs = []
    melbands = []
    w = Windowing(type = 'hann')
    spectrum = Spectrum()
    mfcc = MFCC()
    for frame in FrameGenerator(audio, frameSize=1024, hopSize=512, startFromZero=True):
        mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
        mfccs.append(mfcc_coeffs)
        melbands.append(mfcc_bands)

    # transpose to have it in a better shape
    # we need to convert the list to an essentia.array first (== numpy.array of floats)
    mfccs = essentia.array(mfccs).T
    melbands = essentia.array(melbands).T

    plotPath = joinPath(plotsFolder, fileName)
    fig = plt.figure()
    # and plot
    plt.imshow(melbands[:,:], aspect = 'auto', origin='lower', interpolation='none')
    plt.title("Mel band spectral energies in frames")
    plt.savefig(joinPath(plotPath, 'MelBandSpectralEnergiesInFrames.png'))

    plt.imshow(mfccs[1:,:], aspect='auto', origin='lower', interpolation='none')
    plt.title("MFCCs in frames")
    plt.savefig(joinPath(plotPath,'MFCCsInFrames.png'))

    plt.close(fig)
    
def runTutorial03():
    ComputingMelBandsEnergiesMFCCsInFrames('HotlineBling')
    ComputingMelBandsEnergiesMFCCsInFrames('adaSahilleri')