import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0


def findRandomMove(validMoves):
    """
    A function that returns a random move in a list of valid moves
    """
    # print('Random move.......')
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs, validMoves):
    """
    A function that returns the best move in a list of valid moves
    """
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = -CHECKMATE
    best_player_move = None
    random.shuffle(validMoves)

    for player_move in validMoves:
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()

        for opponent_move in opponent_moves:
            gs.make_move(opponent_move)
            if gs.is_checkmate:
                score = -CHECKMATE
            elif gs.is_stalemate:
                score = STALEMATE
            else:
                score = -turn_multiplier * board_evaluation(gs)
            gs.undo_move()

            if score > opponent_min_max_score:
                opponent_min_max_score = score
                best_player_move = player_move

        # if gs.is_checkmate:
        #     score = CHECKMATE
        # elif gs.is_stalemate:
        #     score = STALEMATE
        # else:
        #     score = turn_multiplier * board_evaluation(gs)
        #
        # gs.undo_move()
        #
        # if score > opponent_min_max_score:
        #     opponent_min_max_score = score
        #     best_player_move = player_move

    return best_player_move


def board_evaluation(games_state):
    """
    A function that evaluates the position for a player at the current game_state
    """
    score = 0
    for row in games_state.board:
        for piece in row:
            if piece.is_white:
                score += piece_score[piece.get_type()[1]]

            elif str(piece) == '--':
                continue
            else:
                score -= piece_score[piece.get_type()[1]]

    return score


def minimax_non_recursive(gs, valid_moves):
    """
    a non-recursive implementation of the minimax algorithm
    """
    turn_multiplier = 1 if gs.white_to_move else -1
    opponent_min_max_score = CHECKMATE
    best_player_move = None

    random.shuffle(valid_moves)

    for player_move in valid_moves:
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()

        opponent_max_score = -CHECKMATE

        for opponent_move in opponent_moves:
            gs.make_move(opponent_move)
            if gs.is_checkmate:
                score = -turn_multiplier * CHECKMATE
            elif gs.is_stalemate:
                score = STALEMATE
            else:
                score = -turn_multiplier * board_evaluation(gs)

            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()

        if opponent_max_score < opponent_min_max_score:
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move

        gs.undo_move()

    return best_player_move
