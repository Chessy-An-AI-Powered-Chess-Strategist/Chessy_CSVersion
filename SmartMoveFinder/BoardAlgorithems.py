from numba import jit

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

@jit
def board_evaluation(games_state):
    score = 0
    for row in games_state.board:
        for piece in row:
            if piece[0] == 'w':
                score += piece_score[piece[1]]
            elif piece[0] == 'b':
                score -= piece_score[piece[1]]

    return score
