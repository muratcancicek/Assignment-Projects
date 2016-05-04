# python_othello
This is a base construct for Othello in Python. It is specifically designed for CS331 at Oregon State Univeristy for the Minimax problem, but could be suited to just playing a game of Othello.

#How to
1. You will need python and pip ([https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py)).
2. You will need to `pip install enum34` 
3. Running the game is simply `python GameDriver.py <player type> <player type>` with a default of a 4x4 board, or you can specify the board size `python GameDriver.py <player type> <player type> <num cols> <num rows>` 
4. `human` and `minimax` are the only valid player types. This can be modified by adding more to the `GameDriver.py` `__init__` function.
