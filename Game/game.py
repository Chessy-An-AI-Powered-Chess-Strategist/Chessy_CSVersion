from Game.settings import gui_settings
from Game.graphicsUserInterface import GraphicsUserInterface
import pygame as p
# Engine imports
from Logic import GameState
import Engine.SmartMoveFinderTest as smf
from SmartPlayer import Engine


p.init()


# define player states
is_player_white_human = True
is_player_black_human = True


def main():
    """
    Main function to run the chess game.
    """
    graphics = GraphicsUserInterface(gui_settings)
    game_state = GameState()

    engine = Engine(game_state) if not is_player_black_human or not is_player_white_human else None

    running = True
    while running:
        human_turn = ((game_state.white_to_move and is_player_white_human) or
                      (not game_state.white_to_move and is_player_black_human))

        running = graphics.handle_events(game_state)
        graphics.draw_game_state(game_state)

        if running and not human_turn:
            # move = smf.minimax_non_recursive(game_state, game_state.get_valid_moves_advanced())
            move = engine.find_best_move_tree(game_state, game_state.get_valid_moves())
            if move is None:
                # print("No move found")
                move = smf.findRandomMove(game_state.get_valid_moves_advanced())

            graphics.make_move(game_state, move, engine)





