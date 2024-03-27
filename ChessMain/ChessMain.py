import pygame as p
from ChessEngine.GameState import GameState

from ChessMain.gui import gui_settings

p.init()


def main():
    screen = p.display.set_mode((gui_settings["WIDTH"], gui_settings["HEIGHT"]))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        draw_game_state(screen, gs)
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



