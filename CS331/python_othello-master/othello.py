from GameDriver import *
import sys             
#sys.argv = ['G', 'minimax', 3, 'minimax', 1, True]
#sys.argv = ['G', 'minimax', 'minimax']
#sys.argv = ['G','human', 'human']
#sys.argv = ['G','human', 'minimax']
#   execfile('GameDriver.py')
#python othello.py minimax 3 minimax 1 True

if __name__ == "__main__":
    if len(sys.argv) == 3:
        g = GameDriver(sys.argv[1], sys.argv[2], 4, 4)
        g.run()
    elif len(sys.argv) == 5:
        g = GameDriver(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        g.run()
    elif len(sys.argv) == 6:
        g = GameDriver(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), True)
        g.run()
    else:
        sys.exit("Usage: GameDriver.py <player type> <player type>")