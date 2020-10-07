"""
 We the undersigned promise that we have in good faith attempted to follow the principles of pair programming.
 Although we were free to discuss ideas with others, the implementation is our own. We have shared a common
 workspace and taken turns at the keyboard for the majority of the work that we are submitting.
 Furthermore, any non programming portions of the assignment were done independently. We recognize that
 should this not be the case, we will be subject to penalties as outlined in the course syllabus.

Pair Programmer 1 - Cole Ferguson, 10/6/20
Pair Programmer 2 - Ryan Hildebrant, 10/6/20
"""


from lib import abstractstrategy, boardlibrary


class AlphaBetaSearch:
    
    def __init__(self, strategy, maxplayer, minplayer, maxplies=3, 
                 verbose=False):
        """"alphabeta_search - Initialize a class capable of alphabeta search
        problem - problem representation
        maxplayer - name of player that will maximize the utility function
        minplayer - name of player that will minimize the uitlity function
        maxplies- Maximum ply depth to search
        verbose - Output debugging information
        """
        self.maxplies = maxplies
        raise NotImplemented


    def alphabeta(self, state):
        """
        Conduct an alpha beta pruning search from state
        :param state: Instance of the game representation
        :return: best action for maxplayer
        """
        raise NotImplemented

    def cutoff(self, state, ply):
        """
        cutoff_test - Should the search stop?
        :param state: current game state
        :param ply: current ply (depth) in search tree
        :return: True if search is to be stopped (terminal state or cutoff
           condition reached)
        """
        # test for terminal state with state
        return state.is_terminal() or ply >= self.maxplies


    def maxvalue(self, state, alpha, beta, ply):
        """
        maxvalue - - alpha/beta search from a maximum node
        Find the best possible move knowing that the next move will try to
        minimize utility.
        :param state: current state
        :param alpha: lower bound of best move max player can make
        :param beta: upper bound of best move max player can make
        :param ply: current search depth
        :return: (value, maxaction)
        """

        raise NotImplemented
                    
    def minvalue(self, state, alpha, beta, ply):
        """
        minvalue - alpha/beta search from a minimum node
        :param state: current state
        :param alpha:  lower bound on best move for min player
        :param beta:  upper bound on best move for max player
        :param ply: current depth
        :return: (v, minaction)  Value of min action and the action that
           produced it.
        """

        raise NotImplemented



class Strategy(abstractstrategy.Strategy):
    """Your strategy, maybe you can beat Tamara Tansykkuzhina, 
       2019 World Women's Champion
    """

    def __init__(self, *args):
        """
        Strategy - Concrete implementation of abstractstrategy.Strategy
        See abstractstrategy.Strategy for parameters
       """
        
        super(Strategy, self).__init__(*args)
        
        self.search = \
            AlphaBetaSearch(self, self.maxplayer, self.minplayer,
                                   maxplies=self.maxplies, verbose=False)
     
    def play(self, board):
        """
        play(board) - Find best move on current board for the maxplayer
        Returns (newboard, action)
        """
        moves = self.evaluate(board)
        # Find the best action
        board.move()
        raise NotImplemented
    
    def evaluate(self, state, turn = None):
        """
        evaluate - Determine utility of terminal state or estimated
        utility of a non-terminal state
        :param state: Game state
        :param turn: Optional turn (None to omit)
        :return:  utility or utility estimate based on strengh of board
                  (bigger numbers for max player, smaller numbers for
                   min player)
        """
        # determine which players turn is being evaluated
        player = None
        if turn % 2 == 0:
            player = 0
        else:
            player = 1

        # get number of pawns for the specified player
        pawns = state.get_pawnsN()[player]
        kings = state.getkingsN()[player]

        # 1.) set up variables based on game state (from lecture slides)
        # 2.) create conditional block statement to assign heuristic weight values based on player passed in
        # 3.) sum up values and return as the heuristic value of the game state
        raise NotImplemented
        

# Run test cases if invoked as main module
if __name__ == "__main__":
    b = boardlibrary.boards["StrategyTest1"]
    redstrat = Strategy('r', b, 6)
    blackstrat = Strategy('b', b, 6)
    
    print(b)
    (nb, action) = redsttrat.play(b)
    print("Red would select ", action)
    print(nb)
    
    
    (nb, action) = blacstrat.play(b)
    print("Black would select ", action)
    print(nb)
    
 

