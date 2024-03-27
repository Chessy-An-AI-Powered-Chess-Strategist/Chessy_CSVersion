import numpy as np
from typing import Optional
from ChessEngine.Move import Move


class GameState:

    board: np.ndarray
    move_log: list[Move]

    def __init__(self):
        # Board is an 8x8 2d list, each element of the list has 2 characters.
        # The first character represents the color of the piece, 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N', 'P'
        # "--" represents an empty space with no piece.
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        self.move_functions = {
            "p": self.get_pawn_moves,
            "R": self.get_rook_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves
        }

        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        """
        We are assuming all the moves given to this function are always valid

        Will not work with castle, en-passant, pawn promotion
        :param move:
        :return:
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) != 0:
            # if the move_log is not empty, then we can undo the last move
            last_move = self.move_log[-1]
            self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
            self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
            self.move_log = self.move_log[:-1]
            self.white_to_move = not self.white_to_move  # switch turns back

    def get_valid_moves(self):
        return self.get_all_possible_moves()  # ToDo: Implement this method

    def get_all_possible_moves(self):
        """
        All moves without considering checks
        :return:
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]  # get the color of the piece
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)

        return moves

    def get_pawn_moves(self, row, col, moves) -> None:
        if self.white_to_move:
            """White pawn moves"""
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))

                # nested so if the pawn is in the starting position, it can move 2 squares
                if row == 6 and self.board[row - 2][col] == "--":

                    moves.append(Move((row, col), (row - 2, col), self.board))

            # captures
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    """There is an enemy piece to capture to the left"""
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))

            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    """There is an enemy piece to capture to the right"""
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:
            """Black pawn moves"""
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))

                # nested so if the pawn is in the starting position, it can move 2 squares
                if row == 1 and self.board[row + 2][col] == "--":

                    moves.append(Move((row, col), (row + 2, col), self.board))

            # captures
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    """There is an enemy piece to capture to the left"""
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))

            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    """There is an enemy piece to capture to the right"""
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

        # ToDo: Add pawn promotion

    def get_rook_moves(self, row, col, moves) -> None:
        # directions = up, down, left, right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            """Loop through each direction"""
            for i in range(1, 8):
                # potentially move up to 7 rows
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":  # empty space
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # enemy piece
                        # Capture the piece
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break

    def get_knight_moves(self, row, col, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for d in directions:
            """Loop through each direction"""
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]

                if end_piece == "--":  # empty space
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif end_piece[0] != self.board[row][col][0]:  # enemy piece
                    # Capture the piece
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves):
        # directions = up, down, left, right
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            """Loop through each direction"""
            for i in range(1, 8):
                # potentially move up to 7 rows
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":  # empty space
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # enemy piece
                        # Capture the piece
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break

    def get_queen_moves(self, row, col, moves):
        # The queen can move like a rook or a bishop
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))
        for d in directions:
            """Loop through each direction"""
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]

                if end_piece == "--":  # empty space
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif end_piece[0] != self.board[row][col][0]:  # enemy piece
                    # Capture the piece
                    moves.append(Move((row, col), (end_row, end_col), self.board))

