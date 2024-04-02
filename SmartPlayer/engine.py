from .moveFinderTree import MoveFinderTree
from .settings import tree_settings
import random

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


    def find_best_move_tree(self, game_state, valid_moves):

        # Collect best move from the tree
        best_move = self.tree.find_next_best_move(game_state)

        if best_move not in valid_moves:
            best_move = self.find_random_move(valid_moves)

        # move the tree down
        self.tree.move_down(best_move)

        # generate teh next layer
        self.tree.add_next_possible_moves(game_state)

        return best_move

    def record_a_move_made(self, move):
        self.tree.move_down(move, self.game_state)