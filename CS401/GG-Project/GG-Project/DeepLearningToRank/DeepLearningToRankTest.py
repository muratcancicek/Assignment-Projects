from Sparker.Logic.ProductPreferrer import *
from Sparker.Logic.FakeProductGenerator import *
from Sparker.Logic.TrainDataHandler import *
from Sparker.Logic.Trainer import *
from .DeepDataHandler import *

def test0():
    keyword = 'tv_unitesi'
    convertHDFStoPickle(keyword)