from .base.chessPiece import ChessPiece
from ..move import Move
from .void import Void
from Engine.gameState import CastleRights


class King(ChessPiece):
    """
    A representation of a King Chess piece in python
    """
    def __init__(self, is_white: bool, piece_symbol: str = "K"):
        """
        Constructor to initialize new King Chess piece
        """
        super().__init__(is_white, piece_symbol)
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        A function that determines all possible legal moves for the King on the chessboard.
        """
        print("King get moves")

        row, col = start

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

                        if str(end_piece) == '--':
                            moves.append(Move(start, (end_row, end_col), board))
                        else:
                            moves.append(Move(start, (end_row, end_col), board, is_capture=True))
                    else:
                        # revert the move
                        board[row][col] = board[end_row][end_col]
                        board[end_row][end_col] = end_piece

        # check for castling
        rooks = [board[row_1][col_1] for col_1 in [0, 7] for row_1 in [0, 7] if board[row_1][col_1].is_white == self.is_white and board[row_1][col_1].get_type() == 'R' and board[row_1][col_1].is_first_move]
        king = board[row][col]

        # ToDo: Complete implementation of castling
        if king.is_first_move:
            # Check if castling is possible
            for rook in rooks:
                # Check if the squares between the king and rook are empty
                empty_squares = [(row, col - i) for i in range(1, 4)] if rook.col < col else [(row, col + i) for i in range(1, 3)]
                # find which of these squares is under attack
                squares_under_attack = self.squares_under_attack(board, self.is_white)

                if all(board[square[0]][square[1]].get_type() == '--' and not self.is_check(board, square) and square not in squares_under_attack for square in empty_squares):
                    moves.append(Move(start, (row, col - 2 if rook.col < col else col + 2), board, is_castling=True))

        return moves

    def squares_under_attack(self, board, is_white):
        """
        A function that determines which squares are under attack by the opponent of the given color.
        """
        squares_under_attack = []

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece.is_white != is_white and str(piece) != '--':
                    # Get the moves of the opponent's piece
                    opponent_moves = piece.get_moves(board, (row, col), [], [])

                    for move in opponent_moves:
                        squares_under_attack.append(move.end)

        return squares_under_attack

    def is_check(self, board, start):
        """
        A function that returns if the King is in check for the given player
        """
        row, col = start

        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)

        assert len(row_moves) == len(col_moves)

        color = -1 if self.is_white else 1

        # loop though all the directions
        for j in range(len(row_moves)):
            end_row_dir = row_moves[j]
            end_col_dir = col_moves[j]

            for i in range(8):
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
                        is_a_rook_attacking = end_piece.get_type() == 'R' and (end_row == 0 or end_col == 0)  # horizontal or vertical
                        is_a_bishop_attacking = end_piece.get_type() == 'B' and (end_row != 0 and end_col != 0)  # diagonal
                        is_a_pawn_attacking = end_piece.get_type() == "p" and end_row == row + color and (end_col == col + end_col_dir)
                        is_a_queen_attacking = end_piece.get_type() == 'Q'
                        is_there_a_king_there = i == 1 and end_piece.get_type() == 'K'

                        is_check = (is_a_rook_attacking or is_a_bishop_attacking or is_a_pawn_attacking or
                                    is_a_queen_attacking or is_there_a_king_there)

                        if is_check:
                            print("King is in check")
                            return True
                else:
                    break

                # ToDo: Implement Knight checks
                # Check for knight checks
                knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
                for m in knight_moves:
                    end_row = row + m[0]
                    end_col = col + m[1]

                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        end_piece = board[end_row][end_col]

                        if end_piece.is_white != self.is_white and end_piece.get_type() == 'N':
                            return True

        return False

    def get_pinned_pieces(self, board, start):
        """
        A function that returns the pinned pieces on the baord for the given plqyer
        """
        pinned_pieces = []

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

        color = -1 if self.is_white else 1

        # loop though all the directions
        for j in range(len(row_moves)):
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
                        is_a_rook_attacking = end_piece.get_type() == 'R' and (
                                    end_row == 0 or end_col == 0)  # horizontal or vertical
                        is_a_bishop_attacking = end_piece.get_type() == 'B' and (
                                    end_row != 0 and end_col != 0)  # diagonal
                        is_a_pawn_attacking = end_piece.get_type() == "p" and end_row == row + color and (
                                    end_col == col + end_col_dir)
                        is_a_queen_attacking = end_piece.get_type() == 'Q'
                        is_there_a_king_there = i == 1 and end_piece.get_type() == 'K'

                        is_check = (is_a_rook_attacking or is_a_bishop_attacking or is_a_pawn_attacking or
                                    is_a_queen_attacking or is_there_a_king_there)

                        if is_check:
                            print("King is in check")
                            checks.append((end_piece, end_row, end_col))
                else:
                    break

                # ToDo: Implement Knight checks
                # Check for knight checks
                knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
                for m in knight_moves:
                    end_row = row + m[0]
                    end_col = col + m[1]

                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        end_piece = board[end_row][end_col]

                        if end_piece.is_white != self.is_white and end_piece.get_type() == 'N':
                            checks.append((end_piece, end_row, end_col))

        return checks
