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

from math import inf


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
        self.maxplayer = maxplayer
        self.minplayer = minplayer
        self.strategy = strategy
        self.maxplies = maxplies


    def alphabeta(self, state):
        """
        Conduct an alpha beta pruning search from state
        :param state: Instance of the game representation
        :return: best action for maxplayer
        """
        """ Look at potential captures """
        max_p_capture_action = state.get_actions(self.maxplayer)[0][1]
        actions = state.get_actions(self.maxplayer)
        max_p_can_capture = ( len(max_p_capture_action) == 3 )

        if max_p_can_capture:
            return max_p_capture_action

        # v = self.maxvalue(state, -inf, inf, 1)
        print(state)
        return self.maxvalue(state, -inf, inf, 1)[1]

    def cutoff(self, state, ply):
        """
        cutoff_test - Should the search stop?
        :param state: current game state
        :param ply: current ply (depth) in search tree
        :return: True if search is to be stopped (terminal state or cutoff
           condition reached)
        """
        t = state.is_terminal()[0]
        p = ply >= self.maxplies
        return state.is_terminal()[0] or ply >= self.maxplies


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
        max_action = None
        if self.cutoff(state, ply):
            v = self.strategy.evaluate(state)
        else:
            v = -inf
            if ply % 2 == 0:
                player = self.minplayer
            else:
                player = self.maxplayer
            for action in state.get_actions(player):
                v = max(v, self.minvalue(state.move(action), alpha, beta, ply + 1)[0])
                max_action = action
                alpha = max(alpha, v)
                if alpha >= beta:
                    break
        return v, max_action

                    
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
        max_action = None
        if self.cutoff(state, ply):
            v = self.strategy.evaluate(state)
        else:
            v = inf
            if ply % 2 == 0:
                player = self.minplayer
            else:
                player = self.maxplayer
            for action in state.get_actions(player):
                v = min(v, self.maxvalue(state.move(action), alpha, beta, ply + 1)[0])
                max_action = action
                alpha = min(alpha, v)
                if alpha <= beta:
                    break
        return v, max_action


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
        action = self.search.alphabeta(board)
        return board.move(action), action


    def evaluate(self, state, turn = None):
        """
        evaluate - Determine utility of terminal state or estimated
        utility of a non-terminal state
        :param state: Game state
        :param turn: Optional turn (None to omit)
        :return:  utility or utility estimate based on strength of board
                  (bigger numbers for max player, smaller numbers for
                   min player)

        Takes a CheckerBoard and turn and determines the strength
        related to the maxplayer given in the constructor. For example,
        a strong red board should return a high score if the constructor
        was invoked with ‘r’, and a low score with ‘b’. The optional argument
        turn may be used to enhance your evaluation function for a specific
        player’s turn, but may be ignored if you do not want to create a turn
        specific evaluation function.
        """
        """ Weights """
        weight_num_pawn = .5
        weight_num_king = .5
        weight_king_dist = 5

        """ Pawn Differences """
        # pawn_dif=      max player pawns - min player pawns
        pawn_diff = state.get_pawnsN()[0] - state.get_pawnsN()[1]
        # king_dif=      max player kings - min player kings
        king_diff = state.get_kingsN()[0] - state.get_kingsN()[1]

        """ Distance to be King """
        max_p_dist_sum = 0
        min_p_dist_sum = 0
        # find the distances from being king for each pawn
        for r, c, piece in state:
            if piece is self.maxplayer:
                max_p_dist_sum += state.disttoking(self.maxplayer, r)
            if piece is self.minplayer:
                min_p_dist_sum += state.disttoking(self.minplayer, r)

        # larger sums -> smaller values
        if max_p_dist_sum != 0:
            max_p_dist_sum = 1 / max_p_dist_sum
        if min_p_dist_sum != 0:
            min_p_dist_sum = 1 / min_p_dist_sum

        dist_diff = max_p_dist_sum - min_p_dist_sum

        # # If red-favored board
        # if self.maxplayer is 'r':
        #     assert (pawn_diff + king_diff + dist_diff) > 0
        # else:
        #     assert (pawn_diff + king_diff + dist_diff) < 0

        # Return sum of each aspect of our evaluation multiplied by its weight
        return pawn_diff * weight_num_pawn +\
               king_diff * weight_num_king +\
               dist_diff * weight_king_dist
        # 1.) set up variables based on game state (from lecture slides)
        # 2.) create conditional block statement to assign heuristic weight values based on player passed in
        # 3.) sum up values and return as the heuristic value of the game state
        

# Run test cases if invoked as main module
if __name__ == "__main__":
    b = boardlibrary.boards["EndGame1"]
    redstrat = Strategy('r', b, 8)
    result = redstrat.evaluate(b)
    print(redstrat.search.alphabeta(b))
    # blackstrat = Strategy('b', b, 6)
    #
    # print(b)
    # (nb, action) = redstrat.play(b)
    # print("Red would select ", action)
    # print(nb)
    #
    #
    # (nb, action) = blackstrat.play(b)
    # print("Black would select ", action)
    # print(nb)
    
 

