
class Monk(object):
    def __init__(self, row):
        self.features = row[1:]
        self.classLabel = 1 if (row[1] != row[2] and row[6] == 1) else 0

    def  __getitem__(self, index):
        return self.features[index]

    def __str__(self):
        return 'ClassLabel = ' + str(self.classLabel) + ' | ' + ' | Features = ' + str(self.features)
    def __repr__(self):
        return 'ClassLabel = ' + str(self.classLabel) + ' | ' + ' | Features = ' + str(self.features)