from .base.chessPiece import ChessPiece
from ..move import Move


class Queen(ChessPiece):
    """
    A representaiton of a queen in python
    """
    def __init__(self, is_white: bool, piece_symbol: str = "Q"):
        super().__init__(is_white, piece_symbol)

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        A function that determines all possible moves to be made at the current game state
        by a queen on the board for a given player (white or black) and appends it to self.moves.
        """
        self.get_moves1(self, board, start, moves, pinned_pieces)
        self.get_moves2(self, board, start, moves, pinned_pieces)

    def get_moves1(self, board, start, moves, pinned_pieces):
        """
        A function that determines all possible moves to be made at the current game state
        by all bishops on the board for a given player (white or black) and appends it to self.moves.
        """
        is_pin = False
        pin_direction = ()
        row, col = start

        for i in range(len(pinned_pieces) - 1, -1, -1):
            if pinned_pieces[i][0] == row and pinned_pieces[i][1] == col:
                is_pin = True
                pin_direction = (pinned_pieces[i][2], pinned_pieces[i][3])
                pinned_pieces.remove(pinned_pieces[i])
                break

        # directions = up-left, up-right, down-right, down-left
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))
        enemy_color = "b" if self.is_white else "w"

        for d in directions:
            """Loop through each direction"""
            for i in range(1, 8):
                # potentially move up to 7 rows
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not is_pin or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = board[end_row][end_col]

                        if end_piece == "--":  # empty space
                            moves.append(Move((row, col), (end_row, end_col), board))
                        elif end_piece[0] == enemy_color:  # enemy piece
                            # Capture the piece
                            moves.append(Move((row, col), (end_row, end_col), board, True))
                            break
                        else:
                            break

    def get_moves2(self, board, start, moves, pinned_pieces):
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
