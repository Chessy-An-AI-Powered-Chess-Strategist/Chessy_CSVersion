from .void import Void
from .base.chessPiece import ChessPiece
from ..move import Move


class Pawn(ChessPiece):
    def __init__(self, is_white: bool, piece_symbol: str = "p"):
        super().__init__(is_white, piece_symbol)
        self.is_pawn_promotion = False

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        Get all possible moves for the pawn
        """
        row, col = start

        direction = -1 if self.is_white else 1

        if self in pinned_pieces:
            return

        # move forward by one
        if 0 <= row + direction < 8:

            # Check if next move will result in a promotion
            if row + direction == 0 or row + direction == 7:
                self.is_pawn_promotion = True

            # Move forward if the square is empty
            if str(board[row + direction][col]) == '--':
                moves.append(Move(start, (row + direction, col), board, is_pawn_promotion=self.is_pawn_promotion))

            # check for enemy pieces for capture on the right
            if 0 <= col + 1 < 8 and board[row + direction][col + 1].is_white != self.is_white:

                # don't append if its an empty square
                if not (board[row + direction][col + 1].is_white is None):
                    moves.append(Move(start, (row + direction, col + 1), board, is_capture=True,
                                      is_pawn_promotion=self.is_pawn_promotion))


            # check for enemy pieces for capture on the left
            if 0 <= col - 1 < 8 and board[row + direction][col - 1].is_white != self.is_white:

                # don't append if it's an empty square
                if not (board[row + direction][col - 1].is_white is None):
                    moves.append(Move(start, (row + direction, col - 1), board, is_capture=True,
                                      is_pawn_promotion=self.is_pawn_promotion))

        # Move forward again if it's the first move
        if self.is_first_move and 0 <= row + 2 * direction < 8:

            # Move forward if the two squares are empty
            if str(board[row + direction][col]) == '--' and str(board[row + 2 * direction][col]) == '--':
                moves.append(Move(start, (row + 2 * direction, col), board))
