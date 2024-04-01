import numpy as np
from .pieces import *
from .pieces.base.chessPiece import ChessPiece
from .move import Move


class GameState:
    board: list[list[ChessPiece]]
    move_log: list[Move]

    def __init__(self):
        # Set up the board
        row1 = [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False), Rook(False)]
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
        self.in_check = False

        self.pinned_pieces = []

    def make_move(self, move: Move):
        print("Making move")

        # check for pawn promotion
        if move.piece_moved.get_type()[1] == "p" and (move.end_row == 0 or move.end_row == 7):
            print("Pawn promotion")
            move.piece_moved = Queen(move.piece_moved.is_white)

        self.board[move.end_row][move.end_col] = move.piece_moved
        self.board[move.start_row][move.start_col] = Void()
        self.move_log.append(move)

        self.white_to_move = not self.white_to_move

        # record moving form piece
        move.piece_moved.piece_moved()

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

    def get_valid_moves(self):
        pinned_pieces = []
        valid_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.is_white == self.white_to_move:
                    piece.get_moves(self.board, (row, col), valid_moves, pinned_pieces)

        # ToDo: Implement the logic for only valid moves

        return valid_moves





