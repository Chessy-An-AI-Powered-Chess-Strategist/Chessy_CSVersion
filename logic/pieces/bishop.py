from .base.chess_piece import ChessPiece
from ..move import Move


class Bishop(ChessPiece):
    """
    A representation of a bishop in python
    """
    def __init__(self, is_white: bool, piece_symbol: str = "B"):
        super().__init__(is_white, piece_symbol)

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        A function that determines all possible moves to be made at the current game state
        by all bishops on the board for a given player (white or black) and appends it to self.moves.
        """
        is_pin = False
        pin_direction = ()
        row, col = start

        if self in pinned_pieces:
            return

        # directions = up-left, up-right, down-right, down-left
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))

        for d in directions:
            """Loop through each direction"""
            for i in range(1, 8):
                # potentially move up to 7 rows
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not is_pin or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = board[end_row][end_col]

                        if str(end_piece) == "--":  # empty space
                            moves.append(Move((row, col), (end_row, end_col), board))
                        elif end_piece.is_white != self.is_white:  # enemy piece
                            # Capture the piece
                            moves.append(Move((row, col), (end_row, end_col), board, True))
                            break
                        else:
                            break
