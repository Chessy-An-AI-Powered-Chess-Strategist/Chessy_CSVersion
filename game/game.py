"""
Game file
"""
# imports
from logic import GameState
import pygame as p
# import Engine.SmartMoveFinderTest as smf
from smart_player import Engine
from game.settings import gui_settings
from game.graphics_user_interface import GraphicsUserInterface

#  initialize pygame object
p.init()


# define player states
is_player_white_human = False
is_player_black_human = False


def main() -> None:
    """
    Entry point for the chess game.

    Initializes the graphical user interface, game state, and engine based on player types.
    Manages the game loop, handling player moves and updating the GUI accordingly.
    """
    graphics = GraphicsUserInterface(gui_settings)
    game_state = GameState()

    engine = Engine(game_state) if not is_player_black_human or not is_player_white_human else None

    running = True
    while running:
        cond1 = game_state.white_to_move and is_player_white_human
        cond2 = not game_state.white_to_move and is_player_black_human
        human_turn = cond1 or cond2
        running = graphics.handle_events(game_state)
        graphics.draw_game_state(game_state)

        if running and not human_turn:
            # move = smf.minimax_non_recursive(game_state, game_state.get_valid_moves_advanced())
            move = engine.find_best_move_tree(game_state, game_state.get_valid_moves_advanced())

            graphics.make_move(game_state, move, engine)


if __name__ == '__main__':

    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['Game', 'pygame', 'Logic', 'Engine', 'SmartPLayer'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
