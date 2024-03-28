# importing required packages
import numpy as np
import pygame as p
from ChessEngine.GameState import GameState
from ChessEngine.Move import Move
import ChessEngine.SmartMoveFinderTest as smf
from ChessMain.gui import gui_settings
from SmartMoveFinder.Engine import Engine

p.init()
p.mixer.init()


def main():
    """
    A function that serves as the brain of the Chess Game. It displays the board and pieces and contains a while loop.
    This function initializes the game state, handles player input, updates the game state based on player actions,
    and draws the game state on the screen. The game loop runs until the player quits the game or closes the window.
    The player can make moves by clicking on squares on the board, undo moves using the 'z' key, and view valid moves
    by highlighting pieces on the board.

    Instance Atrributes:

    screen:


    """
    screen = p.display.set_mode((gui_settings["WIDTH"], gui_settings["HEIGHT"]))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = GameState()
    engine = Engine(game_state)

    start_sound = p.mixer.Sound("game_start.mp3")
    start_sound.play()

    # Sound related state variables
    end_sound_played = False

    # ToDo: Must move this to tree
    valid_moves = game_state.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move

    running, game_over = True, False

    # AI related inputs
    is_player_white_human = False
    is_player_black_human = False

    sq_selected = ()
    player_clicks = []
    while running:
        human_turn = (game_state.white_to_move and is_player_white_human) or (not game_state.white_to_move and is_player_black_human)

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                """handle the mouse click event"""
                if not game_over and human_turn:
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
<<<<<<< Updated upstream
                        # print(move_object)
                        for i in range(len(valid_moves)):
                            if move_object == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made, animate = True, True
                                # reset the player clicks
                                sq_selected = ()
                                player_clicks = []

                        if not move_made:
=======

                        if move_object in valid_moves:
                            move_object = [move for move in valid_moves if move.move_id == move_object.move_id][0]
                            game_state.make_move(move_object)
                            move_made, animate = True, True
                            # reset the player clicks
                            sq_selected = ()
                            player_clicks = []

                        else:
>>>>>>> Stashed changes
                            player_clicks = [sq_selected]

            elif e.type == p.KEYDOWN:
                """key handler"""
                if e.key == p.K_z:
                    game_state.undo_move()
                    move_made = True  # regenerating the valid moves after undoing a move

                if e.key == p.K_r:
                    game_state = GameState()
                    valid_moves = game_state.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False

        # AI move finder logic
        if not game_over and not human_turn:
            move = engine.find_best_move_tree(game_state, valid_moves)
            # move = smf.findRandomMove(valid_moves)
            if move is None:
                move = smf.findRandomMove(valid_moves)
            game_state.make_move(move)
            move_made = True
            animate = True

        if move_made:
            """update the valid moves"""
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)
                animate = False

            valid_moves = game_state.get_valid_moves()

            if game_state.in_check:
                check_sound = p.mixer.Sound("check.mp3")
                check_sound.play()

            elif game_state.move_log[-1].is_capture:
                capture_sound = p.mixer.Sound("capture.mp3")
                capture_sound.play()

            else:
                move_sound = p.mixer.Sound("move.mp3")
                move_sound.play()

            move_made = False

        draw_game_state(screen, game_state, sq_selected)

        if game_state.is_checkmate:

            if not end_sound_played:
                end_sound = p.mixer.Sound("game_end.mp3")
                end_sound.play()
                end_sound_played = True

            game_over = True
            if game_state.white_to_move:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")

        elif game_state.is_stalemate:

            if not end_sound_played:
                end_sound = p.mixer.Sound("game_end.mp3")
                end_sound.play()
                end_sound_played = True

            game_over = True
            draw_text(screen, "Stalemate")

        clock.tick(gui_settings["MAX_FPS"])
        p.display.flip()

def draw_game_state(screen, gs, sq_selected=()):
    draw_board(screen)
    # ToDo: add in piece highlighting or move suggestions
    highlight_squares(screen, gs, gs.get_valid_moves(), sq_selected)
    draw_pieces(screen, gs.board)


def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):  # sq_selected is a piece that can be moved
            s = p.Surface((gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"]))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color("blue"))
            screen.blit(s, (c*gui_settings["SQ_SIZE"], r*gui_settings["SQ_SIZE"]))
            s.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col*gui_settings["SQ_SIZE"], move.end_row*gui_settings["SQ_SIZE"]))



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


def animate_move(move, screen, board, clock):
    delta_row = move.end_row - move.start_row
    delta_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(delta_row) + abs(delta_col)) * frames_per_square

    for frame in range(frame_count + 1):
        r, c = (move.start_row + delta_row*frame/frame_count, move.start_col + delta_col*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        # erase the piece from its ending square
        color = p.Color("white") if (move.end_row + move.end_col) % 2 == 0 else p.Color("light blue")
        end_square = p.Rect(move.end_col*gui_settings["SQ_SIZE"], move.end_row*gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"])
        p.draw.rect(screen, color, end_square)
        # draw captured piece back
        if move.piece_captured != "--":
            screen.blit(gui_settings["IMAGES"][move.piece_captured], end_square)
        # draw moving piece
        screen.blit(gui_settings["IMAGES"][move.piece_moved], p.Rect(int(c*gui_settings["SQ_SIZE"]), int(r*gui_settings["SQ_SIZE"]), gui_settings["SQ_SIZE"], gui_settings["SQ_SIZE"]))
        p.display.flip()
        clock.tick(60)

def draw_text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, 0, p.Color("Black"))
    text_location = p.Rect(0, 0, gui_settings["WIDTH"], gui_settings["HEIGHT"]).move(gui_settings["WIDTH"]/2 - text_object.get_width()/2, gui_settings["HEIGHT"]/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color("Gray"))
    screen.blit(text_object, text_location.move(2, 2))
