#!/usr/bin/env python
__author__ = "Emmitt Johnson"
__credits__ = ["Emmitt Johnson"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "johnemmi@oregonstate.edu"

#pip install enum34
from enum import Enum
import sys
class Direction(Enum):
    __order__ = 'N NE E SE S SW W NW'
    N  = 0
    NE = 1
    E  = 2
    SE = 3
    S  = 4
    SW = 5
    W  = 6
    NW = 7
    
class Board:
    def __init__(self, *args):
        if len(args) == 2:
            self._num_cols = args[0]
            self._num_rows = args[1]
            self.grid = ['.'] * args[0]
            for i in range(len(self.grid)):
                self.grid[i] = ['.'] * args[1]
        elif len(args) == 1:
            board = args[0]
            self._num_cols = board._num_cols
            self._num_rows = board._num_rows
            self.grid = ['.'] * board._num_cols
            for i in range(len(board.grid)):
                self.grid[i] = ['.'] * board._num_rows
            for i in range(len(board.grid)):
                for j in range(len(board.grid[i])):
                    self.grid[i][j] = board.grid[i][j]
        else:
            sys.exit("Board: Incorrect __init__ usage")
    def delete_grid(self):
        self.grid = []
    def get_cell(self, col, row):
        if self.is_in_bounds(col, row):
            return self.grid[col][row]       
    def set_cell(self, col, row, char):
        if self.is_in_bounds(col, row):
            self.grid[col][row] = char 
    def is_cell_empty(self, col, row):
        if self.is_in_bounds(col, row):
            return self.grid[col][row] == '.'
    def is_in_bounds(self, col, row):
        if col >= 0 and col < self._num_cols and row >= 0 and row < self._num_rows:
            return True
        else: 
            return False
    def get_num_rows(self):
        return self._num_rows
    def get_num_cols(self):
        return self._num_cols
    def display(self):
        screen = ""
        for i in range(self._num_rows):
            screen += str(i) + ":| " 
            for j in range(self._num_cols):
                screen += self.get_cell(j, i) + " "
            screen += '\n'
        screen +=  "   -"
        for i in range(self._num_cols):
            screen += "--"
        screen += "\n    "
        for i in range(self._num_cols):
            screen += str(i) + " "
        screen += "\n\n"
        print screen
    def __str__(self):
        return str(self.grid)
    def __repr__(self):
        return str(self.grid)