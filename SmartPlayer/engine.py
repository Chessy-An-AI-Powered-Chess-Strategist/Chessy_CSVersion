from .moveFinderTree import MoveFinderTree
import random

class Engine:

    tree: MoveFinderTree

    def __init__(self, game_state):
        self.tree = MoveFinderTree(game_state, self, game_state.white_to_move)
        self.game_state = game_state

        # make the tree for the depth we need
        for _ in range(3):
            self.tree.add_next_possible_moves(game_state, self)

    def findRandomMove(self, validMoves):
        return validMoves[random.randint(0, len(validMoves)-1)]


    def find_best_move_tree(self, game_state, valid_moves):

        best_move = self.tree.find_next_best_move(game_state, self)
        # best_move = self.findRandomMove(valid_moves)

        self.tree.add_next_possible_moves(game_state, self)
        # print("depth:", self.tree.get_depth())
        self.record_a_move_made(best_move)
        return best_move

    def record_a_move_made(self, move):
        self.tree.move_down(move, self.game_state)