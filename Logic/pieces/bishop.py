from .base.chessPiece import ChessPiece


class Bishop(ChessPiece):
    def __init__(self, is_white: bool, piece_symbol: str = "B"):
        super().__init__(is_white, piece_symbol)


    def get_moves(self, board, start, moves, pinned_pieces):
        pass