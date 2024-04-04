from logic.pieces.base.chess_piece import ChessPiece
from logic import GameState

pawn_eval_white = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

pawn_eval_black = list(reversed(pawn_eval_white))

knight_eval = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

bishop_eval_white = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

bishop_eval_black = list(reversed(bishop_eval_white))

rook_eval_white = [
    [0, 0, 0, 5, 5, 0, 0, 0],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

rook_eval_black = list(reversed(rook_eval_white))

queen_eval = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20],
]

king_eval_white = [
    [20, 30, 10, 0, 0, 10, 30, 20],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, -30, -30, -40, -40, -30, -30, -20],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
]

king_eval_black = list(reversed(king_eval_white))

piece_values = {
    "p": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "k": 1000  # High value to represent the importance of the King
}


def is_under_attack(piece_position: tuple[int, int], is_white: bool, board: list[list[ChessPiece]]) -> bool:
    """Check if a piece is under attack by any enemy piece"""
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col].is_white != is_white and board[row][col].get_type() != "--":
                moves = []
                board[row][col].get_moves(board, (row, col), moves, [])
                for move in moves:
                    if move.end_row == piece_position[0] and move.end_col == piece_position[1]:
                        return True
    return False


def is_protected(piece_position: tuple[int, int], is_white: bool, board: list[list[ChessPiece]]) -> bool:
    """Check if a piece is protected by any friendly piece"""
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col].is_white == is_white and board[row][col].get_type() != "--":
                moves = []
                board[row][col].get_moves(board, (row, col), moves, [])
                for move in moves:
                    if move.end_row == piece_position[0] and move.end_col == piece_position[1]:
                        return True
    return False

def is_attacking(piece_position: tuple[int, int], is_white: bool, board: list[list[ChessPiece]]) -> bool:
    """Check if a piece can attack any enemy piece"""
    row, col = piece_position
    if board[row][col].is_white == is_white and board[row][col].get_type() != "--":
        moves = []
        board[row][col].get_moves(board, (row, col), moves, [])
        for move in moves:
            if board[move.end_row][move.end_col].is_white != is_white:
                return True
    return False


def get_piece_score(piece_position: tuple[int, int], is_white: bool, board: list[list[ChessPiece]]) -> int:
    """Get the value of the current piece ignoring postion on the board"""
    score = 0

    if is_under_attack(piece_position, is_white, board):
        score -= 30
    if is_protected(piece_position, is_white, board):
        score += 30
    if is_attacking(piece_position, is_white, board):
        score += 50
    piece = board[piece_position[0]][piece_position[1]]

    if piece.get_type() == "wp":
        score += pawn_eval_white[piece_position[0]][piece_position[1]]
    if piece.get_type() == "bp":
        score += pawn_eval_black[piece_position[0]][piece_position[1]]
    if piece.get_type() == "N":
        score += knight_eval[piece_position[0]][piece_position[1]]
    if piece.get_type() == "wB":
        score += bishop_eval_white[piece_position[0]][piece_position[1]]
    if piece.get_type() == "bB":
        score += bishop_eval_black[piece_position[0]][piece_position[1]]
    if piece.get_type() == "wR":
        score += rook_eval_white[piece_position[0]][piece_position[1]]
    if piece.get_type() == "bR":
        score += rook_eval_black[piece_position[0]][piece_position[1]]
    if piece.get_type() == "Q":
        score += queen_eval[piece_position[0]][piece_position[1]]
    if piece.get_type() == "wK":
        score += king_eval_white[piece_position[0]][piece_position[1]]
    if piece.get_type() == "bK":
        score += king_eval_black[piece_position[0]][piece_position[1]]

    return score


def board_evaluation(game_state: GameState) -> int:
    """Get the score of a postion on the board"""
    score = 0
    board = game_state.board

    for row in range(0, 8):
        for col in range(0, 8):
            piece = board[row][col]
            if piece.get_type() != "--" and game_state.white_to_move == piece.is_white:
                score += piece_values[piece.get_type()]
                score += get_piece_score((row, col), piece.is_white, board)

    return score

