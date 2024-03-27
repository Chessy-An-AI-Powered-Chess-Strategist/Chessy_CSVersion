import numpy as np
import pygame as p
from ChessEngine.GameState import GameState
from ChessEngine.Move import Move

from ChessMain.gui import gui_settings

p.init()


def main():
    screen = p.display.set_mode((gui_settings["WIDTH"], gui_settings["HEIGHT"]))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = GameState()

    # ToDo: Must move this to tree
    valid_moves = game_state.get_valid_moves()
    move_made = False  # flag variable for when a move is made

    running = True
    sq_selected = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                """handle the mouse click event"""
                # print(len(player_clicks))
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0]//gui_settings["SQ_SIZE"]
                row = location[1]//gui_settings["SQ_SIZE"]

                # save into sq_selected
                if sq_selected == (row, col):
                    # deselect
                    sq_selected = ()
                    player_clicks = []
                else:
                    # select
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                # Check if the player has clicked twice to make a move
                if len(player_clicks) == 2:
                    move_object = Move(player_clicks[0], player_clicks[1], game_state.board)
                    # print(move_object)

                    if move_object in valid_moves:
                        game_state.make_move(move_object)
                        move_made = True

                        # reset the player clicks
                        sq_selected = ()
                        player_clicks = []

                    else:
                        player_clicks = [sq_selected]

            elif e.type == p.KEYDOWN:
                """key handler"""
                if e.key == p.K_z:
                    game_state.undo_move()
                    move_made = True  # regenerating the valid moves after undoing a move

        if move_made:
            """update the valid moves"""
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_game_state(screen, game_state)
        clock.tick(gui_settings["MAX_FPS"])
        p.display.flip()


def draw_game_state(screen, gs):
    draw_board(screen)
    # ToDo: add in piece highlighting or move suggestions
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("light blue")]
    for r in range(gui_settings["DIMENSION"]):
        for c in range(gui_settings["DIMENSION"]):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*gui_settings["SQ_SIZE"], r*gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"]))


def draw_pieces(screen, board):
    for r in range(gui_settings["DIMENSION"]):
        for c in range(gui_settings["DIMENSION"]):
            piece = board[r][c]
            if piece != "--":
                screen.blit(gui_settings["IMAGES"][piece], p.Rect(c*gui_settings["SQ_SIZE"], r*gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"]))



