"""
The main python file which starts the game.
"""
from __future__ import annotations
from Game import main
# from SmartPlayer import Engine
# from Logic import GameState


def run() -> None:
    """
    A function to run the Chess Game
    """
    main()




if __name__ == '__main__':
    run()

    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['Game', 'SmartPlayer', 'Logic'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
