class Move:
    """
    A representation of a Move in a chess game

    Instance Attributes:
        - ranks_to_rows: A dictionary mapping each rank on Chess.com to it's corresponding row in GameState.board
        - rows_to_ranks: A dictionary mapping each row in GameState.board to it's corresponding rank on Chess.com
        - files_to_cols: A dictionary mapping each file letter on Chess.com to it's corresponding row in GameState.board
        - cols_to_files: A dictionary mapping each row in GameState.board to its corresponding file letter on Chess.com

    Representation Invariants:
        - len(ranks_to_rows) == 8
        - len(rows_to_ranks) == 8
        - len(files_to_cols) == 8
        - len(files_to_cols) == 8
    """
    # Positioning data for board and moves
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, enpessant_possbile = False) -> None:
        """
        A constructor that initializes a new Move object
        """
        # print(start_sq, end_sq)
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]

        # Collect the piece moved and captured
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        # check for pawn promotion
        self.is_pawn_promotion = False

        # check for enpessant move
        self.is_enpessant_move = enpessant_possbile

        if self.piece_moved == 'wp' and self.end_row == 0 or self.piece_moved == 'bp' and self.end_row == 7:
            self.is_pawn_promotion = True

        # create a move id (4 digits)
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other) -> bool:  # Overriding the equality operator to compare two moves
        """A function that returns if two moves are the same"""
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def __str__(self) -> str:  # Overriding the string representation of the move
        """A function that returns the chess notation of the given move"""
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col) -> str:
        """
        A function that returns the rank file corresponding to the given row and column
        """
        return self.cols_to_files[col] + self.rows_to_ranks[row]
