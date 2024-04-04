import copy

import numpy as np
from .pieces import *
from .pieces.base.chess_piece import ChessPiece
from .move import Move


class GameState:
    board: list[list[ChessPiece]]
    move_log: list[Move]

    def __init__(self):
        # Set up the board
        row1 = [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False),
                Rook(False)]
        row2 = [Pawn(False) for _ in range(8)]
        row3 = [Void() for _ in range(8)]
        row4 = [Void() for _ in range(8)]
        row5 = [Void() for _ in range(8)]
        row6 = [Void() for _ in range(8)]
        row7 = [Pawn(True) for _ in range(8)]
        row8 = [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)]

        self.board = [row1, row2, row3, row4, row5, row6, row7, row8]

        # Create the move log
        self.move_log = []

        self.white_to_move = True
        self.is_checkmate = False
        self.is_stalemate = False

        # enpassant coord
        self.enpassant_coord = ()

        self.in_check = False

        self.pinned_pieces = []

        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

    def make_move(self, move: Move):

        # check for pawn promotion
        if move.piece_moved.get_type()[1] == "p" and (move.end_row == 0 or move.end_row == 7):
            move.piece_moved = Queen(move.piece_moved.is_white)

        self.board[move.end_row][move.end_col] = move.piece_moved
        self.board[move.start_row][move.start_col] = Void()
        self.move_log.append(move)

        # check if its an enpassant move
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = Void()

        self.white_to_move = not self.white_to_move

        # update enpassant coordinate if two pawn advance
        if move.piece_moved.get_type()[1] == "p" and abs(move.start_row - move.end_row) == 2:
            self.enpassant_coord = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_coord = ()

        # record moving form piece
        move.piece_moved.piece_moved()

        # check to move kings
        if move.piece_moved.get_type()[1] == "K":
            # print("King move detected")
            if move.piece_moved.is_white:
                self.white_king_location = (move.end_row, move.end_col)
            else:
                self.black_king_location = (move.end_row, move.end_col)

        # check if the move is castling
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # right side castle
                rook_location = (7, 7) if move.piece_moved.is_white else (0, 7)
                # move rook to the left of the king
                self.board[move.end_row][move.end_col - 1] = self.board[rook_location[0]][rook_location[1]]
                self.board[rook_location[0]][rook_location[1]] = Void()

            else:  # left side castle
                rook_location = (7, 0) if move.piece_moved.is_white else (0, 0)
                # move rook to the right of the king
                self.board[move.end_row][move.end_col + 1] = self.board[rook_location[0]][rook_location[1]]
                self.board[rook_location[0]][rook_location[1]] = Void()

        # check for checkmate
        # self.get_valid_moves_advanced()

    def undo_move(self):
        if len(self.move_log) == 0:
            return

        move = self.move_log.pop()
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured
        move.piece_moved.revert_move()
        self.white_to_move = not self.white_to_move

        # check to revert pawn promotion
        if move.is_pawn_promotion:
            self.board[move.start_row][move.start_col] = Pawn(move.piece_moved.is_white)

        # check to revert enpassant move
        if move.is_enpassant_move:
            self.board[move.end_row][move.end_col] = Void()
            self.board[move.start_row][move.end_col] = move.piece_captured
            self.enpassant_coord = (move.end_row, move.end_col)

        # check to revert castling move
        if move.is_castle_move:

            # check to remove castling move
            if move.end_col - move.start_col == 2:  # king side
                rook_location = (7, 7) if move.piece_moved.is_white else (0, 7)

                self.board[rook_location[0]][rook_location[1]] = self.board[move.end_row][move.end_col - 1]
                self.board[move.end_row][move.end_col - 1] = Void()

            else:  # queen side
                rook_location = (7, 0) if move.piece_moved.is_white else (0, 0)

                self.board[rook_location[0]][rook_location[1]] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = Void()

        # keep track of the king's location
        if move.piece_moved.get_type()[1] == "K":
            if move.piece_moved.is_white:
                self.white_king_location = (move.start_row, move.start_col)
            else:
                self.black_king_location = (move.start_row, move.start_col)

    def get_valid_moves(self, pinned_pieces):
        valid_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.is_white == self.white_to_move:
                    piece.get_moves(self.board, (row, col), valid_moves, pinned_pieces)

        return valid_moves

    def get_kings_location(self):
        return self.white_king_location if self.white_to_move else self.black_king_location

    def get_valid_moves_advanced(self):
        pinned_pieces = []
        valid_moves = []

        kings_location = self.get_kings_location()

        # print("The kings location", kings_location)
        assert self.board[kings_location[0]][kings_location[1]].get_type()[1] == "K"

        king_piece = self.board[kings_location[0]][kings_location[1]]

        # collect pinned_pieces
        pinned_pieces = king_piece.get_pinned_pieces(self.board, kings_location)


        # if the king is in check
        if king_piece.is_check(self.board, kings_location):
            checks = king_piece.get_checks(self.board, kings_location, pinned_pieces)
            self.in_check = True
            # print("The checks in the game", checks)

            if len(checks) == 1:
                piece_checking = checks[0]
                check_row, check_col = piece_checking[0], piece_checking[1]

                # collect the list of all moves
                valid_moves = self.get_valid_moves(pinned_pieces)
                # print("-----")

                for valid_move in copy.deepcopy(valid_moves):
                    print(str(valid_move), )

                    # make the move
                    self.make_move(valid_move)

                    new_kings_location = self.get_kings_location()

                    if king_piece.is_check(self.board, new_kings_location):
                        valid_moves.remove(valid_move)

                    new_kings_location = kings_location
                    new_kings_piece = king_piece

                    # undo move
                    self.undo_move()

            else:  # if its a double check
                king_piece.get_moves(self.board, kings_location, valid_moves, pinned_pieces)

        else:
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    # check specifically for enpassant moves
                    if piece.get_type() == "wp" or "bp":
                        if (row + 1, col + 1) == self.enpassant_coord and self.board[row + 1][col + 1].is_white != self.white_to_move:
                            valid_moves.append(Move(start_sq=(row, col), end_sq=(row + 1, col + 1), board=self.board,
                                                    is_enpassant_move=True))

                        if (row + 1, col - 1) == self.enpassant_coord and self.board[row + 1][col - 1].is_white != self.white_to_move:
                            valid_moves.append(Move(start_sq=(row, col), end_sq=(row + 1, col - 1), board=self.board,
                                                    is_enpassant_move=True))

                        if (row - 1, col + 1) == self.enpassant_coord and self.board[row - 1][col + 1].is_white != self.white_to_move:
                            valid_moves.append(Move(start_sq=(row, col), end_sq=(row - 1, col + 1), board=self.board,
                                                    is_enpassant_move=True))

                        if (row - 1, col - 1) == self.enpassant_coord and self.board[row - 1][col - 1].is_white != self.white_to_move:
                            valid_moves.append(Move(start_sq=(row, col), end_sq=(row - 1, col - 1), board=self.board,
                                                    is_enpassant_move=True))

                    if piece.is_white == self.white_to_move:
                        piece.get_moves(self.board, (row, col), valid_moves, pinned_pieces)

        if len(valid_moves) == 0:
            if king_piece.is_check(self.board, kings_location):
                self.is_checkmate = True
                # print("Checkmate")
            else:
                self.is_stalemate = True
                # print("Stalemate")

        return valid_moves


    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += str([piece.get_type() for piece in row])
            board_str += "\n"
        return board_str
