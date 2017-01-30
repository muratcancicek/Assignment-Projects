
VALUE_CHECKING = '__VC__'
FEATURE_CHECKING = '__FC__'
class DecisionCondition(object):
    def __init__(self, *args):
        if args[0] == VALUE_CHECKING: # x[i] == value
            self.condition = args[0]
            self.leftFeatureIndex = args[1]
            self.conditionValue = args[2]
        if args[0] == FEATURE_CHECKING: # x[i] == x[j]
            self.condition = args[0]
            self.leftFeatureIndex = args[1]
            self.rightFeatureIndex = args[2]

    def __call__(self, monk):
        if self.condition == VALUE_CHECKING:
            return monk[self.leftFeatureIndex] == self.conditionValue
        if self.condition == FEATURE_CHECKING:
            return monk[self.leftFeatureIndex] == monk[self.rightFeatureIndex]

    def __eg__(self, other):
        if other == None: return False  
        return self.condition == other.condition and self.leftFeatureIndex == other.leftFeatureIndex and self.rightFeatureIndex == other.rightFeatureIndex and self.conditionValue == other.conditionValue 
    def __ne__(self, other):
        return not self.__eg__(other)

    def __my_str__(self):
        if self.condition == VALUE_CHECKING:
            return 'Is x' + str(self.leftFeatureIndex+1) + ' == ' + str(self.conditionValue) + '?'
        if self.condition == FEATURE_CHECKING:
            return 'Is x' + str(self.leftFeatureIndex+1) + ' == x' + str(self.rightFeatureIndex+1) + '?'
    def __str__(self):
        return self.__my_str__()
    def __repr__(self):
        return self.__my_str__()