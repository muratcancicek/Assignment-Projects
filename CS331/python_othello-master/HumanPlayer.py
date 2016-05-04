#!/usr/bin/env python
__author__ = "Emmitt Johnson"
__credits__ = ["Emmitt Johnson"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "johnemmi@oregonstate.edu"

from OthelloBoard import *
from Player import *

class HumanPlayer(Player):
    def __init__(self, symbol):
        self._symbol = symbol
    def get_move(self, OthelloBoard):
        col = raw_input("Enter col: ")
        row = raw_input("Enter row: ")
        return int(col), int(row)
    def clone(self):
        return HumanPlayer(self._symbol)