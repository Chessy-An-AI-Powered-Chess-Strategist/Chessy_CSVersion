from .base.chessPiece import ChessPiece

from ..move import Move


class Knight(ChessPiece):
    def __init__(self, is_white: bool, piece_symbol: str = "N"):
        super().__init__(is_white, piece_symbol)

    def get_moves(self, board, start, moves, pinned_pieces):

        row, col = start

        if self in pinned_pieces:
            return

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

        for d in directions:
            """Loop through each direction"""
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board[end_row][end_col]

                if str(end_piece) == "--":  # empty space
                    moves.append(Move((row, col), (end_row, end_col), board))
                elif end_piece.is_white != self.is_white:  # enemy piece
                    # Capture the piece
                    moves.append(Move((row, col), (end_row, end_col), board, True))