from Game.settings import gui_settings
from Game.graphicsUserInterface import GraphicsUserInterface
import pygame as p
# Engine imports
from Engine.gameState import GameState
import Engine.SmartMoveFinderTest as smf

p.init()


# define player states
is_player_white_human = False
is_player_black_human = False


def main():
    graphics = GraphicsUserInterface(gui_settings)
    game_state = GameState()

    screen = p.display.set_mode((gui_settings["WIDTH"], gui_settings["HEIGHT"]))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    running = True
    while running:
        human_turn = ((game_state.white_to_move and is_player_white_human) or
                      (not game_state.white_to_move and is_player_black_human))

        running = graphics.handle_events(game_state)
        graphics.draw_game_state(game_state)

        if running and not human_turn:
            move = smf.minimax_non_recursive(game_state, game_state.get_valid_moves())
            if move is None:
                move = smf.findRandomMove(game_state.get_valid_moves())

            graphics.make_move(game_state, move)





