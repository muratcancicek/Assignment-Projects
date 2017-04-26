from FeatureProcesser.FeatureProcesser import *
from FeatureProcesser.FeatureAnalyzer import *
from paths import *
        
def rapKeywords(): return ['rap']

def onlyHipHopKeywords(): return ['hip', 'hop']

def rnbKeywords(): return ['rnb', 'r&b', 'r & b']

def hipHopGenreKeywords(): return rapKeywords() + onlyHipHopKeywords() + rnbKeywords()

def popularGenreKeywords(): return ['pop', 'Alternative', 'lana', 'britney', 'kesha', 'lady gaga', 'marin morris']

def popRockGenreKeywords(): return ['Alternative Rock', 'Pop-Punk', 'Paramore', 'Lavigne', 'reckless']

def classicalGenreKeywords(): return ['Classical', 'Ludovico']

def jazzGenreKeywords(): return ['Jazz', 'Joss Stone', 'Zaz']
 
def isGenre(features, keywords):
    if 'metadata_tags_genre' in features.keys():
        genre = str(features['metadata_tags_genre']).lower()
    else:
        genre = ''
    genre += str(features['metadata_tags_file_name']).lower()
    if isinstance(keywords, str):
        return keywords.lower() in genre# or keywords == genre
    for word in keywords:
        if word.lower() in genre:
            return True
    return False

def listGenre(featuresList, genre):
    if featuresList == None: featuresList = collectFeaturesList()
    for features in featuresList:
        if isGenre(features, genre):
            print_(features['metadata_tags_file_name'])

def countGenresFromStatistics(genres = None, statistics = None):
    if statistics == None: statistics = readFeaturesStatisticsJson() 
    valueSet = statistics["fieldValueSets"]['metadata_tags_genre']
    valueList = statistics["fieldValueLists"]['metadata_tags_genre']
    valueCounts = {key: valueList.count(key) for key in valueSet}
    featuresList = [{'metadata_tags_genre':v} for v in valueSet]
    if genres == None: return valueCounts
    counts = {genre: 0 for genre in genres.keys()}
    for features in featuresList:
        for genreKey, genre in genres.items():
            if isGenre(features, genre):
                counts[genreKey] += valueCounts[features['metadata_tags_genre']]
    return counts

def countGenres(genres, featuresList = None, statistics = None):
    if isinstance(genres, str): genres = {genres: genres}
    if isinstance(genres, list): genres = {genre: genre for genre in genres}
    if featuresList == None:
        return countGenresFromStatistics(genres, statistics)
    counts = {genre: 0 for genre in genres.keys()}
    for features in featuresList:
        for genreKey, genre in genres.items():
            if isGenre(features, genre):
                counts[genreKey] += 1
    return counts

def countArtistsFromStatistics(artists = None, statistics = None):
    if statistics == None: statistics = readFeaturesStatisticsJson() 
    valueSet = statistics["fieldValueSets"]['metadata_tags_artist']
    valueList = statistics["fieldValueLists"]['metadata_tags_artist']
    valueCounts = {key: valueList.count(key) for key in valueSet}
    featuresList = [{'metadata_tags_artist':v} for v in valueSet]
    if artists == None: return valueCounts
    counts = {artist: 0 for artist in artists.keys()}
    for features in featuresList:
        for artistKey, artist in artists.items():
            if isGenre(features, artist):
                counts[artistKey] += valueCounts[features['metadata_tags_artist']]
    return counts

def countGenres(artists, featuresList = None, statistics = None):
    if isinstance(artists, str): artists = {artists: artists}
    if isinstance(artists, list): artists = {artist: artist for artist in artists}
    if featuresList == None:
        return countGenresFromStatistics(artists, statistics)
    counts = {artist: 0 for artist in artists.keys()}
    for features in featuresList:
        for artistKey, artist in artists.items():
            if isGenre(features, artist):
                counts[artistKey] += 1
    return counts

def analyzeGenreCounts():
    featuresList = collectFeaturesList()
    statistics = readFeaturesStatisticsJson() #readFeaturesStatistics(featuresList)
    #genres = {'rap': rapKeywords(), 'onlyHipHop': onlyHipHopKeywords(), 'rnb': rnbKeywords(), 'hipHop': hipHopKeywords()}
    genres = {'hipHop': hipHopGenreKeywords(), 'POP': popularGenreKeywords(), 'PopRock': popRockGenreKeywords(), 'Classical': classicalGenreKeywords(), 'Jazz': jazzGenreKeywords()}
    #genres = ['Paramore', 'Lavigne', 'reckless']
    #counts = countGenres(genres, statistics = statistics)
    counts = countGenres(genres, featuresList)
    print_(counts)

def analyzeGenreLists():
    featuresList = collectFeaturesList()
    listGenre(featuresList, ['Pop'])

def analyzeArtistsCounts():
    counts = countArtistsFromStatistics()
    for a, c in counts.items():
        print_(str(a) + '%' + str(c))

def analyzeGenres():
     analyzeGenreCounts()
     #analyzeGenreLists()
     #analyzeArtistsCounts()