
class Monk(object):
    def __init__(self, row):
        self.features = row[1:]
        self.classLabel = 1 if (row[1] != row[2] and row[6] == 1) else 0

    