#!/usr/bin/env python
__author__ = "Muratcan Cicek"
__credits__ = ["Muratcan Cicek"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "cicekm@oregonstate.edu"

from OthelloBoard import *
import sys 

class BoardNode():
    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            if isinstance(args[0], BoardNode):
                self.currentBoard = OthelloBoard(args[0].currentBoard)
                self.parentNode = args[0]
                self.lastAction = args[1] 
                self.currentBoard.play_move(args[1][0], args[1][1], args[0].getSymbol())
                self.isPlayer1 = not args[0].isFirstPlayer()
                self.depthLimit = args[0].depthLimit
                self.depth = args[0].depth + 1
        elif len(args) == 3:
            if isinstance(args[0], OthelloBoard):
                self.parentNode = None
                self.currentBoard = OthelloBoard(args[0])
                self.isPlayer1 = args[1]
                self.depth = 0
                if args[2] == -1:
                    self.depthLimit = float("inf")
                else:
                    self.depthLimit = args[2] 
            else:
                sys.exit("OthelloBoard: Incorrect __init__ usage")
        else:
            sys.exit("OthelloBoard: Incorrect __init__ usage")
    
    def getParent(self): 
        return self.parentNode
    
    def isRootNode(self): 
        return self.parentNode == None

    def isLeaf(self): 
        return not self.currentBoard.has_legal_moves_remaining(self.getSymbol())

    def getLastAction(self): 
        return self.lastAction

    def isFirstPlayer(self): 
        return self.isPlayer1

    def getSymbol(self): 
        if self.isPlayer1:
            return self.currentBoard.get_p1_symbol()
        else:
            return self.currentBoard.get_p2_symbol()

    def getOppositeSymbol(self):
        if self.isPlayer1:
            return self.currentBoard.get_p2_symbol()
        else:
            return self.currentBoard.get_p1_symbol()

    def minimaxDecision(self):
        _, successor = self.maxValue() 
        return successor.getLastAction()
        
    def utilityValue(self):
        selfScore = self.currentBoard.count_score(self.getSymbol())
        oppositeScore = self.currentBoard.count_score(self.getOppositeSymbol())
        return selfScore - oppositeScore

    def maxValue(self):
        self.getSuccessors()
        if len(self.successors) == 0 or self.depth >= self.depthLimit:
            return self.utilityValue(), None
        else:
            utilityValue = - float("inf")
            self.goodSuccessor = None
            for successor in self.successors:
                minVal, _ = successor.minValue()
                if minVal > utilityValue:
                    utilityValue = minVal 
                    self.goodSuccessor = successor
            return utilityValue, self.goodSuccessor
        
    def minValue(self):
        self.getSuccessors()
        if len(self.successors) == 0 or self.depth >= self.depthLimit:
            return self.utilityValue(), None
        else:
            utilityValue = float("inf")
            self.goodSuccessor = None
            for successor in self.successors:
                maxVal, _ = successor.maxValue()
                if maxVal < utilityValue:
                    utilityValue = maxVal 
                    self.goodSuccessor = successor
            return utilityValue, self.goodSuccessor

    def getSuccessors(self): 
        self.successors = []
        self.getSuccessorMoves()
        for move in self.successorMoves:
            self.successors.append(BoardNode(self, move))
        return self.successors

    def getSuccessorMoves(self): 
        self.successorMoves = []
        currentGrid = self.currentBoard.board.grid
        for row in range(len(currentGrid)):
            for col in range(len(currentGrid[row])):
                if currentGrid[col][row] == '.':
                    if self.currentBoard.is_legal_move(col, row, self.getSymbol()):
                        self.successorMoves.append((col, row))
        return self.successorMoves

    def __str__(self):
     return str(self.currentBoard)
    def __repr__(self):
        return str(self.currentBoard)