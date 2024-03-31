from .base.chessPiece import ChessPiece
from ..move import Move


class Knight(ChessPiece):
    """
    A representation of a Knight in python
    """
    def __init__(self, is_white: bool, piece_symbol: str = "N"):
        super().__init__(is_white, piece_symbol)

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        A function that determines all possible moves to be made at the current game state
        by all knights on the board for a given player (white or black) and appends it to self.moves.
        """
        is_pin = False
        row, col = start
        for i in range(len(pinned_pieces) - 1, -1, -1):
            if pinned_pieces[i][0] == row and pinned_pieces[i][1] == col:
                is_pin = True
                pinned_pieces.remove(pinned_pieces[i])
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for d in directions:
            """Loop through each direction"""
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not is_pin:
                    end_piece = board[end_row][end_col]

                    if end_piece == "--":  # empty space
                        moves.append(Move((row, col), (end_row, end_col), board))
                    elif end_piece[0] != board[row][col][0]:  # enemy piece
                        # Capture the piece
                        moves.append(Move((row, col), (end_row, end_col), board, True))
