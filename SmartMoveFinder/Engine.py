
import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]



def make_move(valid_moves):
    return findRandomMove(valid_moves)