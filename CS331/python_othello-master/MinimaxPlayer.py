#!/usr/bin/env python
__author__ = "Emmitt Johnson"
__credits__ = ["Emmitt Johnson"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "johnemmi@oregonstate.edu"

from OthelloBoard import *
from BoardNode import *
from Player import *

class MinimaxPlayer(Player):
    def __init__(self, symbol, isP1, depthLimit = -1): # -1 means no limit
        self._symbol = symbol
        self.isPlayer1 = isP1
        self.depthLimit = depthLimit

    def get_move(self, OthelloBoard):
        minimaxNode = BoardNode(OthelloBoard, self.isPlayer1, self.depthLimit)
        (col, row) = minimaxNode.minimaxDecision()
        return col, row

    def clone(self):
        return MinimaxPlayer(self._symbol)
