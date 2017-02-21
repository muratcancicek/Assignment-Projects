from essentia.standard import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import essentia
import essentia.essentia_extractor as eex
from paths import *
from JsonIO import *
import yaml

def computingMFCCs(fileName, fileExt = '.mp3', fileFolder = mp3sFolder):
    loader = MonoLoader(filename = joinPath(fileFolder, fileName + '.' + fileExt))
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
    
def compareMFCCLengths():
    #ComputingMFCCs('sampleWAV', 'wav', wavsFolder)
    names = ['HotlineBling', 'adaSahilleri', 'sampleWAV']
    pools = []
    for name in names:
        plotPath = joinPath(plotsFolder, name)
        outputPath = joinPath(plotPath, 'mfcc')
        pools.append(evalJson(outputPath))
    for pool in pools:
        #print len(pool['lowlevel']['mfcc']['mean']), len(pool['lowlevel']['mfcc']['var']), \
        #len(pool['lowlevel']['mfcc_bands']['mean']), len(pool['lowlevel']['mfcc_bands']['var'])
        print len(pool['lowlevel']['mfcc']), len(pool['lowlevel']['mfcc'][0]), \
        len(pool['lowlevel']['mfcc_bands']), len(pool['lowlevel']['mfcc_bands'][0])

def computeMyExtractor(inputFilename, outputFilename, profile = 'all', userOptions = {}):
    if profile == 'all':
        profile = joinPath(extractorProfilesFolder, 'all_config.yaml')
    eex.compute(profile, inputFilename, outputFilename, userOptions)
    
def computeAllMyExtractors(fileName, fileExt = '.mp3', fileFolder = mp3sFolder):
    print 'computingAllMyExtractors for ' + fileName + '...'
    inputFileName = joinPath(fileFolder, fileName + fileExt)
    outputFile = joinPath(joinPath(plotsFolder, fileName), 'Descriptors.yaml')
    computeMyExtractor(inputFileName, outputFile) 
    
def computeAllMyExtractorForTEST():
    computeAllMyExtractors('HotlineBling')
    computeAllMyExtractors('adaSahilleri')
    computeAllMyExtractors('sampleWAV', '.wav', wavsFolder)

def compareMyExtractorForTEST():
    names = ['HotlineBling', 'adaSahilleri', 'sampleWAV']
    pools = []
    for name in names:
        plotPath = joinPath(plotsFolder, name)
        outputPath = joinPath(plotPath, 'Descriptors.yaml')
        yml = open(outputPath, 'r').read()
        pools.append(yaml.load(yml))
    keyList = []
    for pool in pools:
        keyList = []
        s = len(pool.keys())
        ln = str(len(pool.keys()))
        for key, value in pool.items():
            ln += ' ' + str(len(value.keys()))
            s += len(value.keys())
            for k, v in value.items():
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        keyList.append(key + '_' + k + '_' + kk)
                if isinstance(v, list):
                    if k != 'chords_progression':
                        ln += ' ' + str(len(v))
                        s += len(v)
        print ln, ' = ', s
    writeToJson(keyList, joinPath(commonFolder, 'keyList'))