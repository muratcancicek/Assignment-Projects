#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#/* original title data stored as hex encoding to avoid invalid chars
#      this method decodes hex encoded strings */
def unhex(hexStr):
    hexStr.decode('ISO-8859-9')


def normalizeKeyword(keyword):
    if (keyword == None):
        return ''
    keyword.replace('  ', ' ').lower()().trim
    
def getFixedEncodingValue(encoded): 
    #return encoded
    if (encoded == None): return None
    #encoded = encoded.decode("utf-8") 
    #encoded = encoded.encode('unicode-escape')
    

    encoded = encoded.replace('%C4%9E', '?') # ?
    encoded = encoded.replace('%C4%9F', '?') # ?
    encoded = encoded.replace('Ç', 'C') # CH
    encoded = encoded.replace('ç', 'c') # ch
    encoded = encoded.replace('Ö', 'O') # O
    encoded = encoded.replace('ö', 'o') # o
    encoded = encoded.replace('Ü', 'U') # U
    encoded = encoded.replace('ü', 'u') # u
    encoded = encoded.replace('İ', 'I') # I
    encoded = encoded.replace('ı', 'i') # i
    encoded = encoded.replace('Ş', 'S') # S
    encoded = encoded.replace('ş', 's') # s

    encoded = encoded.replace('%C4%9E', '?') # ?
    encoded = encoded.replace('%C4%9F', '?') # ?
    encoded = encoded.replace('%C3%87', 'C') # CH
    encoded = encoded.replace('%C3%A7', 'c') # ch
    encoded = encoded.replace('%C3%96', 'O') # O
    encoded = encoded.replace('%C3%B6', 'o') # o
    encoded = encoded.replace('%C3%9C', 'U') # U
    encoded = encoded.replace('%C3%BC', 'u') # u
    encoded = encoded.replace('%C4%B0', 'I') # I
    encoded = encoded.replace('%C4%B1', 'i') # i
    encoded = encoded.replace('%C5%9E', 'S') # S
    encoded = encoded.replace('%C5%9F', 's') # s
    encoded = encoded.replace('%C5%9F', 's') # s?
    #encoded = encoded.replace('+', ' ') # s?
    return encoded

#def getFixedEncodingValue(encoded):
#    if (encoded == None): return None
#    encoded = encoded.replace('%C3%84%C2%9E', '%C4%9E') # ?
#    encoded = encoded.replace('%C3%84%C2%9F', '%C4%9F') # ?
#    encoded = encoded.replace('%C3%83%C2%87', '%C3%87') # CH
#    encoded = encoded.replace('%C3%83%C2%A7', '%C3%A7') # ch
#    encoded = encoded.replace('%C3%83%C2%96', '%C3%96') # O
#    encoded = encoded.replace('%C3%83%C2%B6', '%C3%B6') # o
#    encoded = encoded.replace('%C3%83%C2%9C', '%C3%9C') # U
#    encoded = encoded.replace('%C3%83%C2%BC', '%C3%BC') # u
#    encoded = encoded.replace('%C3%84%C2%B0', '%C4%B0') # I
#    encoded = encoded.replace('%C3%84%C2%B1', '%C4%B1') # i
#    encoded = encoded.replace('%C3%85%C2%9E', '%C5%9E') # S
#    encoded = encoded.replace('%C3%85%C2%9F', '%C5%9F') # s
#    encoded = encoded.replace('%C3%AF%C2%BF%C2%BD', '%C5%9F') # s?
#    return encoded

def convertTrChars(str): 
    if (str == None): return None
    str = str.replace('\u00FC', 'u')
    str = str.replace('\u00DC', 'U')
    str = str.replace('\u00D6', 'O')
    str = str.replace('\u00F6', 'o')
    str = str.replace('\u015E', 'S')
    str = str.replace('\u015F', 's')
    str = str.replace('\u011E', 'G')
    str = str.replace('\u011F', 'g')
    str = str.replace('\u0131', 'i')
    str = str.replace('\u0130', 'I')
    str = str.replace('\u00E7', 'c')
    str = str.replace('\u00C7', 'C')
    return str

def cleanUpAlpha(str):
    str = str.replace('[^\\p{L0-9]+', ' ').trim
    return str


def convertAscii(str):
    convertTrChars(str).lower().replace('[^a-z0-9]+', '')
    return str


def convertAsciiWithoutTrChars(str):
    str.lower().replace('[^a-z0-9]+', '')
    return str


#def convertAsciiWithTrChars(str):
#    WARNING: CHECK TURKISH CHARACTERS IN THE SCALA CODE


def removeVowels(str):
    convertTrChars(str).replace('[aeiuoAEIOU]+', '')
    return str