'''
@author: mroch
'''

# Game representation and mechanics

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.
import statistics

# Python can load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
from lib.checkerboard import CheckerBoard

"""
 We the undersigned promise that we have in good faith attempted to follow the principles of pair programming.
 Although we were free to discuss ideas with others, the implementation is our own. We have shared a common
 workspace and taken turns at the keyboard for the majority of the work that we are submitting.
 Furthermore, any non programming portions of the assignment were done independently. We recognize that
 should this not be the case, we will be subject to penalties as outlined in the course syllabus.
Pair Programmer 1 - Cole Ferguson, 10/6/20
Pair Programmer 2 - Ryan Hildebrant, 10/6/20
"""

if True:
    import imp
    import sys

    major = sys.version_info[0]
    minor = sys.version_info[1]
    modpath = "lib/__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
    tonto = imp.load_compiled("tonto", modpath)

# human - human player, prompts for input
from lib import human, checkerboard, boardlibrary

import ai

from lib.timer import Timer


def Game(red=human.Strategy, black=tonto.Strategy,
         maxplies=6, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0.
    Returns winning player 'r' or 'b'
    """
    # Variables to improve readability/assist in testing
    player_black = 'b'
    player_red = 'r'
    num_moves = 0
    is_red_turn = True
    if firstmove == 1:
        is_red_turn = False
    # Variables to track if board state is repeated
    previous_board = None
    # Variables to declare the winner
    board = init
    winner = board.is_terminal()[1]

    # If init is None, we create a clean board
    if init is None:
        board = boardlibrary.boards["Pristine"]

    red_strategy = red(player_red, board, maxplies)
    black_strategy = black(player_black, board, maxplies)

    # While game is in progress, continually apply moves for each player
    while board.is_terminal()[0] is False:
        if is_red_turn:
            board = red_strategy.play(board)[0]
            current_board = board
            print(board)
        else:
            board = black_strategy.play(board)[0]
            current_board = board
            print(board)

        if current_board == previous_board:
            if is_red_turn is True:
                winner = 'b'
            else:
                winner = 'r'
            break

        # Check to see if a move is possible by comparing board states
        previous_board = current_board

        # Invert our turn flag
        is_red_turn = not is_red_turn

        if verbose:
            num_moves += 1

    # Grab the current winner (is None if no winner yet)
    if verbose:
        # Grab the current winner (is None if no winner yet)
        winner = board.is_terminal()[1]
        # Check if there is no winner
        if winner is None:
            winner = 'No winner'
        print(winner + " in " + str(num_moves) + " moves.")

    return winner


if __name__ == "__main__":
    # Tonto vs Tonto
    # Game(red=ai.Strategy, black=ai.Strategy, init=boardlibrary.boards["multihop"], maxplies=6, firstmove=0)
    Game(red=ai.Strategy, black=ai.Strategy, init=boardlibrary.boards["Pristine"], maxplies=6, firstmove=1)
