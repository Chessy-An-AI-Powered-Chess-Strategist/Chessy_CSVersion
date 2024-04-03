"""
This module defines the ChessPiece class, which is a foundational component of a chess game application.

The ChessPiece class serves as a base class for various types of chess pieces, providing common attributes and methods
that are shared across all chess pieces. Subclasses should implement the specific movement logic and any additional
unique behavior.

Classes:
    ChessPiece: The base class for all chess pieces in the game.
"""


class ChessPiece:
    """
    A class to represent a chess piece in a game of chess.

    Attributes:
        is_white (bool): Determines the color of the chess piece. True if the piece is white, False if black.
        piece_symbol (str): A single character representing the type of the chess piece (e.g., 'K' for King).
        is_first_move (bool): Flag to indicate if the chess piece has not moved yet. Initialized to True.
        num_of_moves_made (int): Counts the number of moves made by the chess piece.

    Methods:
        __init__(self, is_white: bool, piece_symbol: str): Initializes the ChessPiece with color and symbol.
        __str__(self): Returns the piece symbol when the object is printed.
        get_type(self): Returns a string concatenation of the piece's color ('w' or 'b') and its symbol.
        get_moves(self, board, start, moves, pinned_pieces): Abstract method to be implemented by subclasses,
            calculates the valid moves for the piece. Must be overridden.
        piece_moved(self): Marks the piece as having moved, increments the move counter, and sets `is_first_move`
            to False.
        revert_move(self): Decrements the move counter and, if the piece has not moved, sets `is_first_move` back
            to True.
    """

    is_white: bool
    piece_symbol: str
    is_first_move: bool
    num_of_moves_made: int

    def __init__(self, is_white: bool, piece_symbol: str) -> None:
        """Initialize a ChessPiece with a specified color and symbol."""
        self.is_white = is_white
        self.piece_symbol = piece_symbol
        self.is_first_move = True
        self.num_of_moves_made = 0

    def __str__(self) -> str:
        """Return the piece symbol for string representation of the ChessPiece."""
        return self.piece_symbol

    def get_type(self) -> str:
        """Return a string indicating the piece's color and symbol."""
        color = "w" if self.is_white else "b"
        return color + self.piece_symbol

    def get_moves(self, board, start, moves, pinned_pieces) -> NotImplementedError:
        """Abstract method to be implemented by subclasses for move calculation."""
        raise NotImplementedError("This method must be implemented by a subclass")

    def piece_moved(self) -> None:
        """Update the piece's status to indicate a move has been made."""
        self.is_first_move = False
        self.num_of_moves_made += 1

    def revert_move(self) -> None:
        """Revert the piece's status if a move is undone."""
        self.num_of_moves_made -= 1

        if self.num_of_moves_made == 0:
            self.is_first_move = True


if __name__ == '__main__':

    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['Game', 'SmartPlayer', 'Logic'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
