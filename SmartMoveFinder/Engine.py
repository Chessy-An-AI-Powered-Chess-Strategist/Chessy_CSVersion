from SmartMoveFinder.MovesFinderTree import MovesFinderTree
import random


class Engine:

    piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
    CHECKMATE = 1000
    STALEMATE = 0

    def __init__(self, game_state):
        print("Engine init")
        self.tree = MovesFinderTree(game_state, game_state.white_to_move)


    def findRandomMove(validMoves):
        return validMoves[random.randint(0, len(validMoves)-1)]



    def find_best_move_tree(self, game_state, valid_moves):

        best_move = self.tree.find_best_move(game_state)

        return best_move