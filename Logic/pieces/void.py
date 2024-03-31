from .base.chessPiece import ChessPiece


class Void(ChessPiece):
    def __init__(self):
        super().__init__(None, None)

    def __str__(self):
        return "--"

    def get_moves(self, board, start, moves, pinned_pieces):
        """
        Return null to avoid any errors
        """
        pass