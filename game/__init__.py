"""
Set up the package settings
"""

# imports
from game.settings import gui_settings
from game.game import main
from game.graphics_user_interface import GraphicsUserInterface

__all__ = ["gui_settings", "main", "GraphicsUserInterface"]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['doctest', 'python_ta'],  # Additional imports for doctest and python_ta
        'allowed-io': [],  # No direct I/O operations in this script
        'max-line-length': 120,
        'disable': ['E1136']  # Ignore "Invalid module reference" error E1136
    })