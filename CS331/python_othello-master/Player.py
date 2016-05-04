#!/usr/bin/env python
__author__ = "Emmitt Johnson"
__credits__ = ["Emmitt Johnson"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "johnemmi@oregonstate.edu"

from OthelloBoard import *

class Player():
    def __init__(self, symbol):
        self._symbol = symbol
    def get_symbol(self):
        return self._symbol