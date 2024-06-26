import copy

from .base.chess_piece import ChessPiece
from ..move import Move
from .void import Void
# from Engine.gameState import CastleRights


class King(ChessPiece):
    """
    A representation of a King Chess piece in python
    """
    def __init__(self, is_white: bool, piece_symbol: str = "K"):
        """
        Constructor to initialize new King Chess piece
        """
        super().__init__(is_white, piece_symbol)

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        A function that determines all possible legal moves for the King on the chessboard.
        """
        # print("King get moves")

        row, col = start

        # copy the board
        board = copy.deepcopy(board)

        directions = ((0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))

        color = -1 if self.is_white else 1  # -1 for white, 1 for black

        for i in range(0, 8):
            # build all combinations of moves with the row and col moves
            end_row = row + directions[i][0]
            end_col = col + directions[i][1]

            # Check if the end square is within the board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                # collect piece on the end square
                end_piece = board[end_row][end_col]

                # if peace is not ally ( empty or enemy)
                if end_piece.is_white != self.is_white:

                    new_king_location = (end_row, end_col)

                    # move the king there
                    board[end_row][end_col] = board[row][col]
                    board[row][col] = Void()

                    if not self.is_check(board, new_king_location):
                        # revert the move
                        board[row][col] = board[end_row][end_col]
                        board[end_row][end_col] = end_piece

                        if isinstance(end_piece, Void):
                            moves.append(Move(start, (end_row, end_col), board))
                        else:
                            moves.append(Move(start, (end_row, end_col), board, is_capture=True))
                    else:
                        # revert the move
                        board[row][col] = board[end_row][end_col]
                        board[end_row][end_col] = end_piece

        # check for castling
        for move in self.get_castle_rights(board, start):
            moves.append(move)

    def is_check(self, board, start):
        """
        A function that returns if the King is in check for the given player
        """
        row, col = start

        # copy the board to avoid changing the original board
        board = copy.deepcopy(board)

        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)

        assert len(row_moves) == len(col_moves)

        color = -1 if self.is_white else 1

        # loop though all the directions
        for j in range(len(row_moves)):
            end_row_dir = row_moves[j]
            end_col_dir = col_moves[j]

            for i in range(1, 8):
                end_row = row + end_row_dir * i
                end_col = col + end_col_dir * i

                # check if the end square is within the board
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    # collect peace on the end square
                    end_piece = board[end_row][end_col]
                    # print(str(end_piece), end_row, end_col)

                    # if peace is empty
                    if end_piece.is_white == self.is_white:
                        break

                    # if peace is enemy
                    elif str(end_piece) != '--':

                        # check if the piece is attacking the king
                        is_a_rook_attacking = end_piece.get_type()[1] == 'R' and (
                                end_row == 0 or end_col == 0)  # horizontal or vertical
                        is_a_bishop_attacking = end_piece.get_type()[1] == 'B' and (
                                end_row != 0 and end_col != 0)  # diagonal
                        is_a_pawn_attacking = end_piece.get_type()[1] == "p" and end_row == row + color and (
                                end_col == col + end_col_dir)
                        is_a_queen_attacking = end_piece.get_type()[1] == 'Q'
                        is_there_a_king_there = i == 1 and end_piece.get_type()[1] == 'K'

                        is_check = (is_a_rook_attacking or is_a_bishop_attacking or is_a_pawn_attacking or
                                    is_a_queen_attacking or is_there_a_king_there)

                        if is_check:
                            # print("King is in check")
                            return True
                else:
                    break

        # Check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = row + m[0]
            end_col = col + m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board[end_row][end_col]

                if not isinstance(end_piece, Void) and end_piece.is_white != self.is_white and end_piece.get_type()[1] == 'N':
                    return True

        return False

    def get_pinned_pieces(self, board, start):
        """
        A function that returns the pinned pieces on the baord for the given plqyer
        """
        pinned_pieces = []

        board = copy.deepcopy(board)

        row, col = start

        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)

        assert len(row_moves) == len(col_moves)

        # color = -1 if self.is_white else 1

        # loop though all the directions
        for j in range(len(row_moves)):
            end_row_dir = row_moves[j]
            end_col_dir = col_moves[j]

            for i in range(1, 8):
                end_row = row + end_row_dir * i
                end_col = col + end_col_dir * i

                # check if the end square is within the board
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    # collect peace on the end square
                    end_piece = board[end_row][end_col]
                    # print(str(end_piece), end_row, end_col)

                    # if peace is ally
                    if end_piece.is_white == self.is_white:

                        # if we remove the piece and replace it with void
                        board[end_row][end_col] = Void()

                        # check if the king is in check
                        if self.is_check(board, start):
                            pinned_pieces.append(end_piece)

                        # revert the move
                        board[end_row][end_col] = end_piece

                else:
                    break

        return pinned_pieces

    def get_checks(self, board, start, pinned_pieces):
        """
        A function identifies all potential checks to the King's position on the chessboard.
        """
        checks = []
        row, col = start

        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)

        assert len(row_moves) == len(col_moves)

        board = copy.deepcopy(board)

        color = -1 if self.is_white else 1

        # loop though all the directions
        for j in range(1, 8):
            end_row_dir = row_moves[j]
            end_col_dir = col_moves[j]

            for i in range(8):
                end_row = row + end_row_dir * i
                end_col = col + end_col_dir * i

                # check if the end square is within the board
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    # collect peace on the end square
                    end_piece = board[end_row][end_col]

                    # if peace is empty
                    if end_piece.is_white == self.is_white:
                        break

                    # if peace is enemy
                    elif str(end_piece) != '--':

                        # check if the piece is attacking the king
                        is_a_rook_attacking = end_piece.get_type()[1] == 'R' and (
                                    end_row == 0 or end_col == 0)  # horizontal or vertical
                        is_a_bishop_attacking = end_piece.get_type()[1] == 'B' and (
                                    end_row != 0 and end_col != 0)  # diagonal
                        is_a_pawn_attacking = end_piece.get_type()[1] == "p" and end_row == row + color and (
                                    end_col == col + end_col_dir)
                        is_a_queen_attacking = end_piece.get_type()[1] == 'Q'
                        is_there_a_king_there = i == 1 and end_piece.get_type()[1] == 'K'

                        is_check = (is_a_rook_attacking or is_a_bishop_attacking or is_a_pawn_attacking or
                                    is_a_queen_attacking or is_there_a_king_there)

                        if is_check:
                            print("King is in check")
                            checks.append((end_piece, end_row, end_col))
                else:
                    break

        # Check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = row + m[0]
            end_col = col + m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = board[end_row][end_col]

                if str(end_piece) != '--' and end_piece.is_white != self.is_white and end_piece.get_type()[1] == 'N':
                    checks.append((end_piece, end_row, end_col))

        return checks

    def get_castle_rights(self, board, start):
        """
        A function that returns the current castling rights of the King
        """
        castle_moves = []

        row, col = start  # Kings location on the board

        possible_rook_locations = [(0, 0), (0, 7), (7, 0), (7, 7)]
        all_rooks = [(board[row][col], (row, col)) for row, col in possible_rook_locations if board[row][col].get_type()[1] == 'R']

        all_ally_rooks = [rook for rook in all_rooks if rook[0].is_white == self.is_white]

        # Check if the King has moved
        if not self.is_first_move:
            return []

        # if the king has not moves
        not_moves_rooks = [rook for rook in all_ally_rooks if rook[0].is_first_move]
        # print("Not moved rooks", not_moves_rooks)

        # for all the available rooks
        for rook in not_moves_rooks:
            # check if all the squares between them are empty

            # now the move can be added
            if rook[1][1] > col:  # right rook
                eligible_move = True

                for check_col in range(col + 1, rook[1][1] - 1):
                    # break if it is not empty
                    # print("Checking", row, check_col, board[row][check_col])
                    if str(board[row][check_col]) != '--':
                        # print("Not empty for right rook")
                        eligible_move = False
                        break

                    # break if the king will be in check
                    if self.is_check(board, (row, check_col)):
                        # print("Not uncheck for right rook")
                        eligible_move = False
                        break

                if eligible_move:
                    castle_moves.append(Move(start, (row, col + 2), board, is_castle_move=True))

            else:  # left rook
                eligible_move = True

                for check_col in range(col - 1, rook[1][1] + 1, -1):
                    # break if it is not empty
                    if not isinstance(board[row][check_col], Void):
                        # print("Not uncheck for left rook")
                        eligible_move = False
                        break

                    # break if the king will be in check
                    if self.is_check(board, (row, check_col)):
                        # print("Not uncheck for left rook")
                        eligible_move = False
                        break

                if eligible_move:
                    castle_moves.append(Move(start, (row, col - 3), board, is_castle_move=True))

        # print("Castle moves", castle_moves)

        return castle_moves








