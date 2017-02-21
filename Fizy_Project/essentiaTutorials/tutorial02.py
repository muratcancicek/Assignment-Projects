from essentia.standard import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paths import *

def ComputingSpectrumMelBandsEnergiesMFCCs(fileName):
    loader = MonoLoader(filename = joinPath(mp3sFolder, fileName + '.mp3'))
    # and then we actually perform the loading:
    audio = loader()
    w = Windowing(type = 'hann')
    spectrum = Spectrum()  # FFT() would return the complex FFT, here we just want the magnitude spectrum
    mfcc = MFCC()
    frame = audio[6*44100 : 6*44100 + 1024]
    spec = spectrum(w(frame))
    mfcc_bands, mfcc_coeffs = mfcc(spec)

    plotPath = joinPath(plotsFolder, fileName)
    fig = plt.figure()
    plt.plot(spec)
    plt.title('The spectrum of a frame:')
    plt.savefig(joinPath(plotPath,'TheSpectrumOfAFrame.png'))

    plt.plot(mfcc_bands)
    plt.title('Mel band spectral energies of a frame:')
    plt.savefig(joinPath(plotPath, 'MelBandSpectralEnergiesOfAFrame.png'))

    plt.plot(mfcc_coeffs)
    plt.title('First 13 MFCCs of a frame:')
    plt.savefig(joinPath(plotPath, 'First13MFCCsOfAFrame.png'))
    plt.close(fig)
    
def runTutorial02():
    ComputingSpectrumMelBandsEnergiesMFCCs('HotlineBling')
    ComputingSpectrumMelBandsEnergiesMFCCs('adaSahilleri')