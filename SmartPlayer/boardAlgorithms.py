
piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}


def board_evaluation(game_state):
    turn_multiplier = 1 if game_state.white_to_move else -1
    score = 0

    if game_state.is_checkmate:
        score = -1000
    elif game_state.is_stalemate:
        score = 0
    else:
        for row in game_state.board:
            for piece in row:
                if str(piece) == "--":
                    continue
                elif piece.is_white:
                    score += piece_score[str(piece)]
                else:
                    score -= piece_score[str(piece)]

        score = -turn_multiplier * score

    return score
