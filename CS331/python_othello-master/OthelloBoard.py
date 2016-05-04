#!/usr/bin/env python
__author__ = "Emmitt Johnson"
__credits__ = ["Emmitt Johnson"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "johnemmi@oregonstate.edu"

from Board import *
import sys 

class OthelloBoard(Board):
    def __init__(self, *args, **kwargs):
        if len(args) == 4:
            #col, row, p1_symbol, p2_symbol
            self.board = Board(args[0], args[1])
            self._p1_symbol = args[2]
            self._p2_symbol = args[3]
            self.currentTurn = True
        elif len(args) == 1:
            #OthelloBoard
            self.board = Board(args[0].board)
            self._p1_symbol = args[0]._p1_symbol
            self._p2_symbol = args[0]._p2_symbol
            self.currentTurn = args[0].currentTurn
        else:
            sys.exit("OthelloBoard: Incorrect __init__ usage")
    def initialize(self):
        self.board.set_cell(self.board._num_cols / 2 - 1, self.board._num_rows / 2 - 1, self._p1_symbol)
        self.board.set_cell(self.board._num_cols / 2, self.board._num_rows / 2, self._p1_symbol)
        self.board.set_cell(self.board._num_cols / 2 - 1, self.board._num_rows / 2, self._p2_symbol)
        self.board.set_cell(self.board._num_cols / 2, self.board._num_rows / 2 - 1, self._p2_symbol)
    def set_coords_in_direction(self, col, row, dir):
        if dir == Direction.N:
            next_col = col
            next_row = row + 1
        elif dir == Direction.NE:
            next_col = col + 1;
            next_row = row + 1;
        elif dir == Direction.E:
            next_col = col + 1;
            next_row = row;
        elif dir == Direction.SE:
            next_col = col + 1;
            next_row = row - 1;
        elif dir == Direction.S:
            next_col = col;
            next_row = row - 1;
        elif dir == Direction.SW:
            next_col = col - 1;
            next_row = row - 1;
        elif dir == Direction.W:
            next_col = col - 1;
            next_row = row;
        elif dir == Direction.NW:
            next_col = col - 1;
            next_row = row + 1;
        else:
            next_col = None
            next_row = None   
        return next_col, next_row
    def check_endpoint(self, col, row, symbol, dir, match_symbol):
        if not self.board.is_in_bounds(col, row) or self.board.is_cell_empty(col, row):
            return False
        else:
            if match_symbol:
                if self.board.get_cell(col, row) == symbol:
                    return True
                else:
                    next_col, next_row = self.set_coords_in_direction(col, row, dir)
                    return self.check_endpoint(next_col, next_row, symbol, dir, match_symbol)
            else:
                if self.board.get_cell(col, row) == symbol:
                    return False
                else:
                    next_col, next_row = self.set_coords_in_direction(col, row, dir)
                    return self.check_endpoint(next_col, next_row, symbol, dir, not match_symbol)
    def is_legal_move(self, col, row, symbol):
        result = False
        if not self.board.is_in_bounds(col, row) or not self.board.is_cell_empty(col, row):
            return result
        else:
            for d in Direction:
                next_col, next_row = self.set_coords_in_direction(col, row, d)
                if self.check_endpoint(next_col, next_row, symbol, d, False):
                    result = True
                    break
        return result
    def flip_pieces_helper(self, col, row, symbol, dir):
        if self.board.get_cell(col, row) == symbol:
            return 0
        else:
            self.board.set_cell(col, row, symbol)
            next_col, next_row = self.set_coords_in_direction(col, row, dir)
            return 1 + self.flip_pieces_helper(next_col, next_row, symbol, dir)
    def flip_pieces(self, col, row, symbol):
        pieces_flipped = 0
        if not self.board.is_in_bounds(col, row):
            return None
        for d in Direction:
            next_col, next_row = self.set_coords_in_direction(col, row, d)
            if self.check_endpoint(next_col, next_row, symbol, d, False):
                pieces_flipped += self.flip_pieces_helper(next_col, next_row, symbol, d)
        return pieces_flipped
    def has_legal_moves_remaining(self, symbol):
        for i in range(self.board._num_cols):
            for j in range(self.board._num_rows):
                if self.board.is_cell_empty(i, j) and self.is_legal_move(i, j, symbol):
                    return True
        return False
    def count_score(self, symbol):
        score = 0
        for i in range(self.board._num_cols):
            for j in range(self.board._num_rows):
                if self.board.grid[i][j] == symbol:
                    score += 1
        return score
    def play_move(self, col, row, symbol):
        if self.is_legal_move(col, row, symbol):
            self.currentTurn = not self.currentTurn 
            self.board.set_cell(col, row, symbol)
            self.flip_pieces(col, row, symbol)
    def get_p1_symbol(self):
        return self._p1_symbol
    def get_p2_symbol(self):
        return self._p2_symbol
    def __str__(self):
     return str(self.board.grid)
    def __repr__(self):
        return str(self.board.grid)