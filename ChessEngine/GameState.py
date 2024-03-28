# importing required packages
import numpy as np
from typing import Optional
from ChessEngine.Move import Move
from SmartMoveFinder import Engine


class GameState:
    """
    A Representation of the state of a chess game.

    Instance Attributes:
        - board (np.ndarray): A 2D numpy array representing the chess board.
        - move_log (list[Move]): A list of Move objects representing the moves made in the game.

    Representation Invariants:
        - len(self.board) == 8
        - all(len(self.board[row]) == 8 for row in self.board)
        - 0 <= len(self.move_log) <= 2
    """
    board: np.ndarray
    move_log: list[Move]

    def __init__(self):
        """
        Constructor that initializes a new GameState Object
        """
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

        # game state variables
        self.is_checkmate = False
        self.is_stalemate = False

        # Track teh kings to make checking easier
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        # Make a list of checks and pins
        self.in_check = False
        self.checks = []
        self.pins = []

        self.check_for_pins_and_checks = ((), (), ())

    def make_move(self, move):
        """
        A function that takes in a move object and makes a move on a chessboard.
        (We are assuming all the moves given to this function are always valid)
        (Will not work with castle, en-passant, pawn promotion)
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        # Update the king's location
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        print(
            f"Move made: {move.piece_moved} from {(move.start_row, move.start_col)} to {(move.end_row, move.end_col)}")

    def undo_move(self):
        """
        A function that undoes the most recent move made
        """
        if len(self.move_log) != 0:
            # if the move_log is not empty, then we can undo the last move
            last_move = self.move_log[-1]
            self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
            self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
            self.move_log = self.move_log[:-1]
            self.white_to_move = not self.white_to_move  # switch turns back

            print(
                f"Move undone: {last_move.piece_moved} from {(last_move.start_row, last_move.start_col)} to {(last_move.end_row, last_move.end_col)}")

    def get_valid_moves_try2(self):
        """
        A function that obtains all valid moves on a chessboard that have to do with checks.
        The function works as follows:

        1. Get all possible moves
        2. For each move, make the move
        3. Generate all the opponent's moves
        4. Check if any of the opponent's moves attack the king
        5. If the king is attacked, the move is invalid

        """
        moves = []
        self._check_for_pins_and_checks()
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks

        if self.white_to_move:
            king_row, king_col = self.white_king_location
        else:
            king_row, king_col = self.black_king_location

        # print(f"Getting valid moves for {'white' if self.white_to_move else 'black'}")

        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                check = self.checks[0]
                check_row, check_col = check[0], check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # squares that pieces can move to
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]

                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break

                # get rid of any moves that don't block the check or move the king
                # for i in range(len(self.pins) - 1, -1, -1):
                #     if self.pins[i][0] != check[0] and self.pins[i][1] != check[1]:
                #         del self.pins[i]
                moves = valid_squares

            else:  # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)

        else:
            moves = self.get_all_possible_moves()

        print(f"Valid moves:", [str(move) for move in moves])
        return moves  # ToDo: Implement this method

    def get_valid_moves(self):
        """
        A function that returns a list of all the valid moves that can be made at the current game state
        """
        moves = []
        self._check_for_pins_and_checks()
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks

        king_row, king_col = self.white_king_location if self.white_to_move else self.black_king_location

        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.get_all_possible_moves()

                check = self.checks[0]
                check_row, check_col = check[0], check[1]
                piece_checking = self.board[check_row][check_col]

                valid_squares = []  # squares that pieces can move to

                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:  # capture the piece
                            break

                print(f"Valid moves:", [str(move) for move in moves])

                # get rid of any moves that don't block the check or move the king
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':  # move king to get out of check
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])

            else:  # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()

        print(f"Valid moves:", [str(move) for move in moves])

        if len(moves) == 0:
            if self.in_check:
                self.is_checkmate = True
                print("Checkmate")
            else:
                self.is_stalemate = True
                print("Stalemate")

        return moves

    def get_all_possible_moves(self):
        """
        A function that returns a list of all possible moves other than checks
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
        """
        A function that determines all possible moves to be made at the current game state
        by all pawns on the board for a given player (white or black) and appends it to self.moves.
        """
        # check for pins
        is_pin = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                is_pin = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            """White pawn moves"""
            if self.board[row - 1][col] == "--":

                if not is_pin or pin_direction == (-1, 0):
                    moves.append(Move((row, col), (row - 1, col), self.board))

                    # nested so if the pawn is in the starting position, it can move 2 squares
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(Move((row, col), (row - 2, col), self.board))

            # captures
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    """There is an enemy piece to capture to the left"""
                    if not is_pin or pin_direction == (-1, -1):
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))

            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    """There is an enemy piece to capture to the right"""
                    if not is_pin or pin_direction == (-1, 1):
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else:
            """Black pawn moves"""
            if self.board[row + 1][col] == "--":

                if not is_pin or pin_direction == (1, 0):
                    moves.append(Move((row, col), (row + 1, col), self.board))

                    # nested so if the pawn is in the starting position, it can move 2 squares
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(Move((row, col), (row + 2, col), self.board))

            # captures
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    """There is an enemy piece to capture to the left"""
                    if not is_pin or pin_direction == (1, -1):
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))

            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    """There is an enemy piece to capture to the right"""
                    if not is_pin or pin_direction == (1, 1):
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))

        # ToDo: Add pawn promotion

    def get_rook_moves(self, row, col, moves) -> None:
        """
        A function that determines all possible moves to be made at the current game state
        by all rooks on the board for a given player (white or black) and appends it to self.moves.
        """
        is_pin = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                is_pin = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
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

                    if not is_pin or pin_direction == d or pin_direction == (-d[0], -d[1]):
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
        """
        A function that determines all possible moves to be made at the current game state
        by all knights on the board for a given player (white or black) and appends it to self.moves.
        """
        is_pin = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                is_pin = True
                self.pins.remove(self.pins[i])
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for d in directions:
            """Loop through each direction"""
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not is_pin:
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":  # empty space
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] != self.board[row][col][0]:  # enemy piece
                        # Capture the piece
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves):
        """
        A function that determines all possible moves to be made at the current game state
        by all bishops on the board for a given player (white or black) and appends it to self.moves.
        """
        is_pin = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                is_pin = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # directions = up-left, up-right, down-right, down-left
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))
        enemy_color = "b" if self.white_to_move else "w"

        for d in directions:
            """Loop through each direction"""
            for i in range(1, 8):
                # potentially move up to 7 rows
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not is_pin or pin_direction == d or pin_direction == (-d[0], -d[1]):
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
        """
        A function that determines all possible moves to be made at the current game state
        by a queen on the board for a given player (white or black) and appends it to self.moves.
        """
        # The queen can move like a rook or a bishop
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        """
        A function that determines all possible moves to be made at the current game state
        by a king on the board for a given player (white or black) and appends it to self.moves.
        """
        print("Getting king moves.......")
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"

        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]

                if end_piece[0] != ally_color:
                    # Place the king on the end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_row, end_col)
                        print("New white king location", self.white_king_location)
                    else:
                        self.black_king_location = (end_row, end_col)

                    in_check, pins, checks = self._check_for_pins_and_checks(save_to_cache=False)
                    print("Checking for pins and checks", in_check, pins, checks)

                    if not in_check:
                        print(str(Move((row, col), (end_row, end_col), self.board)))
                        moves.append(Move((row, col), (end_row, end_col), self.board))

                    if ally_color == "w":
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

        # directions = ((0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))
        # for d in directions:
        #     """Loop through each direction"""
        #     end_row = row + d[0]
        #     end_col = col + d[1]
        #
        #     if 0 <= end_row < 8 and 0 <= end_col < 8:
        #         end_piece = self.board[end_row][end_col]
        #
        #         if end_piece == "--":  # empty space
        #             moves.append(Move((row, col), (end_row, end_col), self.board))
        #         elif end_piece[0] != self.board[row][col][0]:  # enemy piece
        #             # Capture the piece
        #             moves.append(Move((row, col), (end_row, end_col), self.board))

    def _check_for_pins_and_checks(self, save_to_cache: Optional[bool] = True):
        """
        A function that determines all pins and checks in the current gamestate by checking which peaces
        are attacking the king in each direction and checking if the king is in check
        """
        pins, checks, in_check = [], [], False
        king_row, king_col = self.white_king_location if self.white_to_move else self.black_king_location

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

                    end_piece = self.board[end_row][end_col]
                    # if end_piece != "--":  # if the square is not empty
                    if end_piece[0] == ("w" if self.white_to_move else "b"):
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
                                (self.white_to_move and 6 <= j <= 7) or (not self.white_to_move and 4 <= j <= 5)))
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
                end_piece = self.board[end_row][end_col]
                print("end_piece", end_piece)

                if end_piece[0] == ("w" if not self.white_to_move else "b") and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))

        print("Returning as", "w" if self.white_to_move else "b", in_check, pins, checks)

        if save_to_cache:
            self.check_for_pins_and_checks = in_check, pins, checks

        return in_check, pins, checks
