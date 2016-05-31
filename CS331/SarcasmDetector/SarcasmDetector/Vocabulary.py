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

class Sentence(MyObject):
    def __init__(self, sentenceLine):
        self.processSentence(sentenceLine[2:-4])
        self.classLabel = int(sentenceLine[-3])
        self.buildString()
        self.current = 0

    def processSentence(self, rawSentence):
        rawSentence = rawSentence.translate(string.maketrans("",""), string.punctuation)
        self.words = []
        for word in rawSentence.split():
            self.words.append(word)

    def buildString(self):
        self.sentenceString  = ''
        for word in self.words:
            self.sentenceString = self.sentenceString + ' ' + word
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
    def __init__(self, label):
        self.label = label
        self.words = {}
        self.sentences = []
        
    def addWord(self, word):
        if not word in self.words.keys():
            self.words[word] = word

    def addSentence(self, sentence): 
        self.sentences.append(sentence)
        for word in sentence:
            self.addWord(word)

    def size(self):
        return len(self.words)

    def sentenceCount(self):
        return len(self.sentences)