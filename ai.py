from lib import abstractstrategy

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
        available_actions = state.get_actions(self.maxplayer)
        if len(available_actions) <= 0:
            return None
        max_p_capture_action = available_actions[0]
        max_p_can_capture = (len(max_p_capture_action[1]) == 3)

        if max_p_can_capture:
            return max_p_capture_action

        """ Enter alpha-beta pruning """
        return self.maxvalue(state, -inf, inf, 1)[1]

    def cutoff(self, state, ply):
        """
        cutoff_test - Should the search stop?
        :param state: current game state
        :param ply: current ply (depth) in search tree
        :return: True if search is to be stopped (terminal state or cutoff
           condition reached)
        """
        return state.is_terminal()[0] or ply >= self.maxplies

    def maxvalue(self, state, alpha, beta, ply):
        """
        maxvalue - - alpha/beta search from a maximum node
        Find the best possible move knowing that the next move will try to
        minimize utility.
        :param state: current state
        :param alpha: lower bound of best move max player can make
        :param beta: upper bound of best move max player can make (at most)
        :param ply: current search depth
        :return: (value, maxaction)
        """
        max_action = None
        if self.cutoff(state, ply):
            v = self.strategy.evaluate(state)
        else:
            v = -inf
            # checks each available action and passes it to min
            for action in state.get_actions(self.maxplayer):
                new_v_value = max(v, self.minvalue(state.move(action), alpha, beta, ply + 1)[0])
                # if our new value is less than v, assign it to v and update the action and alpha
                if new_v_value > v:
                    v = new_v_value
                    alpha = max(alpha, v)
                    max_action = action
                # check if we can prune
                if alpha >= beta:
                    break
        if max_action is None:
            pass
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
        min_action = None
        if self.cutoff(state, ply):
            v = self.strategy.evaluate(state)
        else:
            v = inf
            # checks each available action and passes it to max
            for action in state.get_actions(self.minplayer):
                new_v_value = min(v, self.maxvalue(state.move(action), alpha, beta, ply + 1)[0])
                # if our new value is less than v, assign it to v and update the action and alpha
                if new_v_value < v:
                    v = new_v_value
                    alpha = min(alpha, v)
                    min_action = action
                # check if we can prune
                if alpha <= beta:
                    break
        # if we do not have an action, end the function call
        if min_action is None:
            pass
        return v, min_action


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
        print("Our bot moves " + board.get_action_str(action))
        if action is None:
            return board, None
        return board.move(action), action

    def evaluate(self, state, turn=None):
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
        player_diff = []
        """ Weights """
        weight_num_pawn = 5
        weight_num_king = 8
        weight_king_dist = 3
        weight_edge_piece = 3
        weight_moves_available = 3
        weight_goalie = 4
        weight_king_in_last_row = -4

        """ Amount of moves available """
        max_p_moves = len(state.get_actions(self.maxplayer))
        min_p_moves = len(state.get_actions(self.minplayer))
        player_diff.append(max_p_moves * weight_moves_available)
        player_diff.append(-(min_p_moves * weight_moves_available))

        """ Pawn Differences """
        # pawn_dif=      max player pawns - min player pawns
        pawn_diff = state.get_pawnsN()[0] - state.get_pawnsN()[1]
        player_diff.append(pawn_diff * weight_num_pawn)
        # king_dif=      max player kings - min player kings
        king_diff = state.get_kingsN()[0] - state.get_kingsN()[1]
        player_diff.append(king_diff * weight_num_king)

        """ Distance to be King, Edge Pieces """
        max_p_dist_sum = 0
        min_p_dist_sum = 0

        for r, c, piece in state:
            # Test if any 'goalies' (back row pieces that prevent enemy from king-ing)
            if self.is_goalie(r, state.edgesize, self.maxplayer):
                player_diff.append(weight_goalie)

            """ If this piece:
                  - belongs to maxplayer
                  - is a King
                  - is in the far row/other player's row """
            # If piece belongs to maxplayer
            if state.isplayer(self.maxplayer, piece):
                # If piece is a king
                if state.isking(piece):
                    # If in other player's row (we can just pass in the
                    # other player into is_goalie() to check this)
                    if self.is_goalie(r, state.edgesize, self.minplayer):
                        player_diff.append(weight_king_in_last_row)
            if state.isplayer(self.minplayer, piece):
                # If piece is a king
                if state.isking(piece):
                    # If in other player's row (we can just pass in the
                    # other player into is_goalie() to check this)
                    if self.is_goalie(r, state.edgesize, self.minplayer):
                        player_diff.append(-weight_king_in_last_row)

            # Test if piece is on edge of the board
            if self.is_edge_piece(r, c, state.edgesize):
                # If edge piece is maxplayer's
                if state.isplayer(self.maxplayer, piece):
                    player_weight = 1
                else:
                    player_weight = 0

                player_diff.append(weight_edge_piece * player_weight)

            # Evaluate the approx. distance to be a king
            if state.isplayer(self.maxplayer, piece):
                max_p_dist_sum += state.disttoking(self.maxplayer, r)
            if state.isplayer(self.minplayer, piece):
                min_p_dist_sum += state.disttoking(self.minplayer, r)

        # larger sums -> smaller values
        if max_p_dist_sum != 0:
            max_p_dist_sum = 1 / max_p_dist_sum
        if min_p_dist_sum != 0:
            min_p_dist_sum = 1 / min_p_dist_sum

        dist_diff = max_p_dist_sum - min_p_dist_sum
        player_diff.append(dist_diff * weight_king_dist)
 
        # Return sum of each aspect of our evaluation
        if self.maxplayer == 'r':
            return sum(player_diff)
        else:
            return -sum(player_diff)
        # return pawn_diff * weight_num_pawn +\
        #        king_diff * weight_num_king +\
        #        dist_diff * weight_king_dist

    @staticmethod
    def is_edge_piece(r, c, board_size):
        """
        Determines if the given piece is on the edge of the board
        :param r: row of the piece
        :param c: column of the piece
        :param board_size: total size (in r and c) of the board
        :return: True if in the first or last row/column
        """
        in_first_row = (r - 1) < 0
        in_first_col = (c - 1) < 0
        in_last_row = (r + 1) > (board_size - 1)
        in_last_col = (c + 1) > (board_size - 1)
        return in_first_row or in_first_col \
               or in_last_row or in_last_col

    @staticmethod
    def is_goalie(r, board_size, player):
        """
        Determines if the given row value satisfies the requirement for a "goalie".
        A goalie is a piece that resides in the furthest back row, which prevents the enemy from
        kinging their pieces.
        :param r: row index to evaluate
        :param board_size: total number of rows on the board
        :param player: player that we're evaluating with respect to
        :return: True if the piece is in the furthest row from your opponent.
        """
        in_black_row = (r - 1) < 0
        in_red_row = (r + 1) > (board_size - 1)
        if player == 'r':
            return in_red_row
        if player == 'b':
            return in_black_row
