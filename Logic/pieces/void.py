from .base.chessPiece import ChessPiece


class Void(ChessPiece):

    def __init__(self):
        super().__init__(None, "--")

    def __str__(self):
        return "--"
