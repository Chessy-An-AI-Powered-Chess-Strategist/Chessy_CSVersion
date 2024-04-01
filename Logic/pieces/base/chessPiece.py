class ChessPiece:

    is_white: bool
    piece_symbol: str
    is_first_move: bool
    num_of_moves_made: int

    def __init__(self, is_white: bool, piece_symbol: str):
        self.is_white = is_white
        self.piece_symbol = piece_symbol
        self.is_first_move = True
        self.num_of_moves_made = 0

    def __str__(self):
        return self.piece_symbol

    def get_type(self):
        color = "w" if self.is_white else "b"
        return color + self.piece_symbol

    def get_moves(self, board, start, moves, pinned_pieces):
        raise NotImplementedError("This method must be implemented by a subclass")

    def piece_moved(self):
        self.is_first_move = False
        self.num_of_moves_made += 1

    def revert_move(self):
        self.num_of_moves_made -= 1

        if self.num_of_moves_made == 0:
            self.is_first_move = True
