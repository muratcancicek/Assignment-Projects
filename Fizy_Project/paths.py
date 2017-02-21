import os

def joinPath(prePath, path):
    return os.path.join(prePath, path)

def getAbsolutePath(fileName):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    return joinPath(script_dir, fileName)
   
dataFolder = getAbsolutePath('data')

commonFolder = joinPath(dataFolder, 'common')

extractorProfilesFolder = joinPath(dataFolder, 'extractorProfiles')

plotsFolder = joinPath(dataFolder, 'plots')

soundsFolder = joinPath(dataFolder, 'sounds')
mp3sFolder = joinPath(soundsFolder, 'mp3s')
wavsFolder = joinPath(soundsFolder, 'wavs') 

