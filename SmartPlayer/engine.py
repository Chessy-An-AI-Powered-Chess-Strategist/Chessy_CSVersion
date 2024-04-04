import copy

from .moveFinderTree import MoveFinderTree
from .settings import tree_settings
import random
from .boardAlgorithms import board_evaluation

class Engine:

    tree: MoveFinderTree

    def __init__(self, game_state):
        self.tree = MoveFinderTree(game_state, game_state.white_to_move)
        self.game_state = game_state

        # make the tree for the depth we need
        for _ in range(tree_settings["DEPTH"]):
            self.tree.add_next_possible_moves(game_state)

    def find_random_move(self, valid_Moves):
        return valid_Moves[random.randint(0, len(valid_Moves)-1)]

    def find_best_move_negamax(self, game_state, tree, turn_multiplier):
        next_move = None
        max_score = -1000  # - checkmate

        if tree.is_leaf():
            return None, turn_multiplier * board_evaluation(game_state)

        else:
            random.shuffle(tree.next_valid_moves)
            # print("The next valid moves", tree.next_valid_moves)
            for move in tree.next_valid_moves:

                game_state.make_move(move.move)
                score = -move.find_move_negamax(game_state, -turn_multiplier)[1]

                if score > max_score:
                    max_score = score
                    next_move = tree.move

                    if self.tree.is_root():
                        next_move = move.move

                game_state.undo_move()

            return next_move, max_score


    def find_best_move_tree(self, game_state, valid_moves):

        turn_multiplier = 1 if game_state.white_to_move else -1

        copy_of_game_state = copy.deepcopy(game_state)

        # Collect best move from the tree
        best_move = self.find_best_move_negamax(copy_of_game_state, self.tree, turn_multiplier)[0]

        if best_move not in valid_moves:
            best_move = self.find_random_move(valid_moves)

        # move the tree down
        self.tree.move_down(best_move)

        # generate teh next layer
        self.tree.add_next_possible_moves(game_state)

        return best_move

    def record_a_move_made(self, move):
        self.tree.move_down(move, self.game_state)