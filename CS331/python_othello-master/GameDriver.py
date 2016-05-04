#!/usr/bin/env python
__author__ = "Emmitt Johnson"
__credits__ = ["Emmitt Johnson"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "johnemmi@oregonstate.edu"

from OthelloBoard import *
from Player import *
from HumanPlayer import *
from MinimaxPlayer import *
import sys

class GameDriver:
    def __init__(self, *args, **kwargs):
        if len(args) == 4:
            #p1type, p2type, num_cols, num_rows
            if args[0] == "human":
                self._p1 = HumanPlayer('X')
            elif args[0] == "minimax":
                self._p1 = MinimaxPlayer('X', True)
            else:
                sys.exit("Invalid Player 1 type: " + str(args[0]))

            if args[1] == "human":
                self._p2 = HumanPlayer('O')
            elif args[1] == "minimax":
                self._p2 = MinimaxPlayer('O', False)
            else:
                sys.exit("Invalid Player 2 type: " + str(args[1]))
                
            self._board = OthelloBoard(args[2], args[3], self._p1.get_symbol(), self._p2.get_symbol())
            self._board.initialize()
        elif len(args) == 5:
            #p1type, p2type, num_cols, num_rows
            if args[0] == "human":
                self._p1 = HumanPlayer('X')
            elif args[0] == "minimax":
                self._p1 = MinimaxPlayer('X', True, args[1])
            else:
                sys.exit("Invalid Player 1 type: " + str(args[0]))

            if args[2] == "human":
                self._p2 = HumanPlayer('O')
            elif args[2] == "minimax":
                self._p2 = MinimaxPlayer('O', False, args[3])
            else:
                sys.exit("Invalid Player 2 type: " + str(args[2]))
                
            self._board = OthelloBoard(8, 8, self._p1.get_symbol(), self._p2.get_symbol())
            self._board.initialize()
        elif len(args) == 1:
            self._p1 = args[0]._p1.clone()
            self._p2 = args[0]._p2.clone()
            self._board = OthelloBoard(args[0]._board)
        else:
            sys.exit("GameDriver: Incorrect __init__ usage")
    def run(self):
        toggle = 0;
        cant_move_counter=0;
        current = self._p1;
        opponent = self._p2;
        self._board.board.display();
        print "Player 1 (" + str(self._p1.get_symbol()) + ") move:"
        while True:
            if self._board.has_legal_moves_remaining(current.get_symbol()):
                cant_move_counter = 0
                self.process_move(current, opponent)
            else:
                print "Can't move\n"
                if cant_move_counter == 1:
                    break
                else:
                    cant_move_counter += 1
            self.display()
            self._board.board.display()
            toggle = (toggle + 1) % 2
            if toggle == 0:
                current = self._p1
                opponent = self._p2
                print "Player 1 (" + str(self._p1.get_symbol()) + ") move:"
            else:
                current = self._p2
                opponent = self._p1
                print "Player 2 (" + str(self._p2.get_symbol()) + ") move:"
        self.display()
        if self._board.count_score(self._p1.get_symbol()) == self._board.count_score(self._p2.get_symbol()):
            print "Tie game"
        elif self._board.count_score(self._p1.get_symbol()) > self._board.count_score(self._p2.get_symbol()):
            print "Player 1 wins"
        else:
            print "Player 2 wins"
    def display(self):
        screen = ""
        screen += "Player 1 (" + self._p1.get_symbol() + ") score: " + str(self._board.count_score(self._p1.get_symbol())) + "\n"
        screen += "Player 2 (" + self._p2.get_symbol() + ") score: " + str(self._board.count_score(self._p2.get_symbol()))
        print screen
    def process_move(self, curr_player, opponent):
        invalid_move = True
        while invalid_move:
            col, row = curr_player.get_move(self._board)
            if not self._board.is_legal_move(col, row, curr_player.get_symbol()):
                print "Invalid move.\n"
                continue
            else:
                print "Selected move: col = " + str(col) + ", row = " + str(row) + "\n"
                self._board.play_move(col, row, curr_player.get_symbol())
                invalid_move = False
