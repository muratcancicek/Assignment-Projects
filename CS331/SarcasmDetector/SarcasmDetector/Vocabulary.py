import string 

class MyObject(object):
    def __key__(self):
        return None
    def __lt__(self, other):
        return self.__key__() < other.__key__()
    def __eq__(self, other):
        return self.__key__() == other.__key__()
    def __my_str__(self):
        return super.__str__()
    def __str__(self):
     return self.__my_str__()
    def __repr__(self):
     return self.__my_str__()

class Word(MyObject):
    def __init__(self, word):
        self.string = word.lower()
        self.trueCount = 0 if word == 'classlabel' else 1
        self.falseCount = 0

    def increaseCount(self): 
        self.trueCount += 1

    def setFalseCount(self, columnNumber):  
        self.falseCount = columnNumber - self.trueCount
            
    def __key__(self):
        return self.string
    
    def __lt__(self, other):
        if isinstance(other, str): return self.__key__() < other
        return self.__key__() < other.__key__()
    def __eq__(self, other):
        if isinstance(other, str): return self.__key__() == other
        return self.__key__() == other.__key__()

    def __my_str__(self):
        return self.string + ' (W)'


class Sentence(MyObject):
    def __init__(self, sentenceLine):
        if isinstance(sentenceLine, Sentence):
            self.words = [Word(word.string) for word in sentenceLine.words]
            self.classLabel = int(sentenceLine.classLabel)
            self.sentenceString = str(sentenceLine.sentenceString) 
        else:
            self.processSentence(sentenceLine[2:-4])
            self.classLabel = int(sentenceLine[-3])
            self.buildString()
        self.current = 0

    def processSentence(self, rawSentence):
        rawSentence = rawSentence.translate(string.maketrans("",""), string.punctuation)
        self.words = []
        for word in rawSentence.split():
            self.words.append(Word(word))

    def buildString(self):
        self.sentenceString  = ''
        for word in self.words:
            self.sentenceString = self.sentenceString + ' ' + word.string
        self.sentenceString = str(self.classLabel) + ' |' + self.sentenceString

    def __iter__(self):
        return self

    def next(self): # Python 3: def __next__(self)
        if not self.current < len(self.words):
            self.current = 0
            raise StopIteration
        else:
            item = self.words[self.current]
            self.current += 1
            return item

    def __my_str__(self):
        return self.sentenceString
        
class Vocabulary(MyObject):
    def __init__(self):
        self.words = {}
        self.sentences = []
        
    def addWord(self, word):
        if not word.string in self.words.keys():
            self.words[word.string] = word
        #    self.words[word.string].increaseCount()
        #else:

    def addSentence(self, sentence): 
        self.sentences.append(sentence)
        for word in sentence:
            self.addWord(word)

    def size(self):
        return len(self.words)

    def sentenceCount(self):
        return len(self.sentences)