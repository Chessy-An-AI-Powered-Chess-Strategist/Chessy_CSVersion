from .base.chessPiece import ChessPiece
from ..move import Move


class Rook(ChessPiece):
    def __init__(self, is_white: bool, piece_symbol: str = "R"):
        super().__init__(is_white, piece_symbol)

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        A function that determines all possible moves to be made at the current game state
        by all rooks on the board for a given player (white or black) and appends it to self.moves.
        """

        row, col = start

        # check if the piece is pinned. if so, no possible moves
        if self in pinned_pieces:
            return

        # directions = up, down, left, right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.is_white else "w"

        for d in directions:
            """Loop through each direction"""
            for i in range(1, 8):
                # potentially move up to 7 rows
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:

                    end_piece = board[end_row][end_col]

                    if end_piece == "--":  # empty space
                        moves.append(Move((row, col), (end_row, end_col), board))
                    elif end_piece[0] == enemy_color:  # enemy piece
                        # Capture the piece
                        moves.append(Move((row, col), (end_row, end_col), board, True))
                        break
                    else:
                        break
