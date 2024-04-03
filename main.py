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

    # code to test the tree
    # game_state = GameState()
    #
    # engine = Engine(game_state)

    # print(engine.tree.get_depth())
    #
    # for i in range(20):
    #     next_move = engine.find_best_move_tree(game_state, game_state.get_valid_moves_advanced())
    #
    #     game_state.make_move(next_move)
    #
    #     print("Next_move", next_move)
    #     print(str(game_state))


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
