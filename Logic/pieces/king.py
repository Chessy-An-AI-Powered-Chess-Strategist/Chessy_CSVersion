from .base.chessPiece import ChessPiece
from ..move import Move
from typing import Optional
from Engine.Move import Move


class King(ChessPiece):
    """
    A representation of a King in Python
    """
    def __init__(self, is_white: bool, piece_symbol: str = "K"):
        super().__init__(is_white, piece_symbol)

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        A function that determines all possible moves to be made at the current game state
        by a king on the board for a given player (white or black) and appends it to self.moves.
        """
        row, col = start

        print("Getting king moves.......")
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.is_white else "b"

        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board[end_row][end_col]

                if end_piece[0] != ally_color:
                    # Place the king on the end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                        print("New white king location", self.white_king_location)
                    else:
                        self.black_king_location = (end_row, end_col)

                    in_check, pins, checks = pinned_pieces
                    print("Checking for pins and checks", in_check, pins, checks)

                    if not in_check:
                        print(str(Move((row, col), (end_row, end_col), board)))
                        moves.append(Move((row, col), (end_row, end_col), board))

                    if ally_color == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    def _check_for_pins_and_checks(self, board, save_to_cache: Optional[bool] = True):
        """
        A function that determines all pins and checks in the current gamestate by checking which peaces
        are attacking the king in each direction and checking if the king is in check
        """
        pins, checks, in_check = [], [], False
        king_row, king_col = self.white_king_location if self.is_white else self.black_king_location

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))

        # loop through all the directions of possible checks
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = king_row + d[0] * i
                end_col = king_col + d[1] * i

                # check if the end square is on the board
                if 0 <= end_row < 8 and 0 <= end_col < 8:

                    end_piece = board[end_row][end_col]
                    # if end_piece != "--":  # if the square is not empty
                    if end_piece[0] == ("w" if self.is_white else "b"):
                        """if the piece is an ally"""
                        if possible_pin == ():
                            # Piece could be pinned
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break  # there is no pin or check in this direction

                    elif end_piece != "--":
                        """If the piece is an enemy"""
                        type = end_piece[1]

                        # Check if different pieces could be attacking the king
                        is_a_rook_attacking = (0 <= j <= 3 and type == 'R')
                        is_a_bishop_attacking = (4 <= j <= 7 and type == 'B')
                        is_a_pawn_attacking = (i == 1 and type == 'p' and (
                                (self.is_white and 6 <= j <= 7) or (not self.is_white and 4 <= j <= 5)))
                        is_a_queen_attacking = (type == 'Q')
                        is_there_a_king_there = (i == 1 and type == 'K')

                        # Check if the king is in check
                        is_check = (is_a_rook_attacking or is_a_bishop_attacking or is_a_pawn_attacking or
                                    is_a_queen_attacking or is_there_a_king_there)

                        if is_check and possible_pin == ():
                            in_check = True
                            checks.append((end_row, end_col, d[0], d[1]))
                            # print("King is in check", checks)
                            break

                        elif is_check:
                            pins.append(possible_pin)
                            # print(possible_pin, "is pinned", pins)
                            break

                    # ToDo: Add break statement
                else:
                    break

        # Check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = king_row + m[0]
            end_col = king_col + m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board[end_row][end_col]
                print("end_piece", end_piece)

                if end_piece[0] == ("w" if not self.is_white else "b") and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))

        print("Returning as", "w" if self.is_white else "b", in_check, pins, checks)

        if save_to_cache:
            self.check_for_pins_and_checks = in_check, pins, checks

        return in_check, pins, checks
