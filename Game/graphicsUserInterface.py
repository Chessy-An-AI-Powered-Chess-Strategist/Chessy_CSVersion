import pygame
from Engine.Move import Move
from Logic.pieces import Void
from settings import gui_settings


class GraphicsUserInterface:
    """
    A class that is responsible for the graphics of the game
    """

    def __init__(self, settings: dict):
        self.valid_moves = None
        pygame.init()

        self.settings = settings
        self.screen = pygame.display.set_mode((settings["WIDTH"], settings["HEIGHT"]))
        self.clock = pygame.time.Clock()
        self.screen.fill(pygame.Color("white"))
        pygame.display.flip()

        # select_variables
        self.sq_selected = ()
        self.player_clicks = []

        # play the start sound
        self._play_sound("game_start")
        self.display_selected_highlights = False

    def draw_game_state(self, game_state):
        """
        A function that draws the game state on the screen. It draws the board, the pieces, and the highlights.
        """
        # Clear the screen
        self.screen.fill(pygame.Color("white"))

        # Draw the board
        self._draw_board()
        self._highlight_squares(game_state)
        self._draw_pieces(game_state.board)
        # self.draw_text("Hello")

        if game_state.is_checkmate and game_state.white_to_move:
            self.draw_text("Black wins by checkmate")
        elif game_state.is_checkmate:
            self.draw_text("White wins by checkmate")

        elif game_state.is_stalemate:
            self.draw_text("Stalemate")

        pygame.display.flip()

    def _draw_board(self):
        """
        A function that draws the board on the screen.
        """
        # print("Drawing board...")
        colors = [pygame.Color("white"), pygame.Color("light blue")]
        for r in range(self.settings["DIMENSION"]):
            for c in range(self.settings["DIMENSION"]):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(c * self.settings["SQ_SIZE"], r * self.settings["SQ_SIZE"],
                                             self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))

    def _draw_pieces(self, board):
        """
        A function that draws the pieces on the screen.
        """
        for r in range(self.settings["DIMENSION"]):
            for c in range(self.settings["DIMENSION"]):
                piece = board[r][c]
                if str(piece) != '--':
                    self.screen.blit(self.settings["IMAGES"][piece.get_type()],
                                     pygame.Rect(c * self.settings["SQ_SIZE"], r * self.settings["SQ_SIZE"],
                                                 self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))

    def _highlight_squares(self, game_state):
        """
        A function that highlights the squares at the current game state
        """
        if self.sq_selected != ():
            r, c = self.sq_selected[0], self.sq_selected[1]
            if game_state.board[r][c].is_white == game_state.white_to_move:  # sq_selected is a piece that can be moved
                s = pygame.Surface((self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))
                s.set_alpha(100)  # transparency value
                s.fill(pygame.Color("blue"))
                self.screen.blit(s, (c * self.settings["SQ_SIZE"], r * self.settings["SQ_SIZE"]))

                if not self.display_selected_highlights:
                    self.valid_moves_for_highlights = game_state.get_valid_moves_advanced()
                    self.display_selected_highlights = True

                for move in self.valid_moves_for_highlights:
                    if move.start_row == r and move.start_col == c:
                        if move.is_capture:
                            s.fill(pygame.Color("red"))  # change color to red if the move is a capture move
                        elif move.is_enpassant_move:
                            # print("there is an enpassant move on the board")
                            s.fill(pygame.Color("yellow"))
                        else:
                            s.fill(pygame.Color("yellow"))
                        self.screen.blit(s, (
                            move.end_col * self.settings["SQ_SIZE"], move.end_row * self.settings["SQ_SIZE"]))
        # if self.sq_selected != ():
        #     r, c = self.sq_selected[0], self.sq_selected[1]
        #     if game_state.board[r][c].is_white == game_state.white_to_move:  # sq_selected is a piece that can be moved
        #         s = pygame.Surface((self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))
        #         s.set_alpha(100)  # transparency value
        #         s.fill(pygame.Color("blue"))
        #         self.screen.blit(s, (c * self.settings["SQ_SIZE"], r * self.settings["SQ_SIZE"]))
        #         s.fill(pygame.Color("yellow"))
        #         for move in game_state.get_valid_moves():
        #             if move.start_row == r and move.start_col == c:
        #                 self.screen.blit(s, (
        #                 move.end_col * self.settings["SQ_SIZE"], move.end_row * self.settings["SQ_SIZE"]))

    def handle_events(self, game_state):
        """
        A function that handles the events in the game.
        """
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False  # Exit the game

            elif e.type == pygame.MOUSEBUTTONDOWN:
                # print(len(player_clicks))
                location = pygame.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // self.settings["SQ_SIZE"]
                row = location[1] // self.settings["SQ_SIZE"]

                # save into sq_selected
                if self.sq_selected == (row, col):
                    # deselect
                    self.sq_selected = ()
                    self.player_clicks = []
                    self.display_selected_highlights = False
                else:
                    # select
                    self.display_selected_highlights = False
                    self.sq_selected = (row, col)
                    self.player_clicks.append(self.sq_selected)

                # Check if the player has clicked twice to make a move
                if len(self.player_clicks) == 2:
                    self.make_move(game_state, Move(self.player_clicks[0], self.player_clicks[1], game_state.board))

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    self._undo_move(game_state)
        return True  # Tell running to continue

    def make_move(self, game_state, move_object, engine=None):
        """
        A function that makes a move in the game.
        """
        self.valid_moves = game_state.get_valid_moves_advanced()

        # print("move object", move_object)
        for i in range(len(self.valid_moves)):

            # print("i:", self.valid_moves[i])
            if str(move_object) == str(self.valid_moves[i]):
                # print("valid_move:", self.valid_moves[i])

                move_object.is_capture = self.valid_moves[i].is_capture

                # print(self.valid_moves[i])
                game_state.make_move(self.valid_moves[i])

                # animate move
                self._animate_move(game_state, self.valid_moves[i])
                # print(game_state.board)
                # print(self.valid_moves_for_highlights)

                # display the move
                self.draw_game_state(game_state)

        # reset the player clicks
        self.sq_selected = ()
        self.player_clicks = []

    def _undo_move(self, game_state):
        """
        A function that undoes a move in the game and draws the changes to the board.
        """
        game_state.undo_move()
        self.draw_game_state(game_state)

    def _animate_move(self, game_state, move):
        """
        A function that animates the move in the game.
        """
        delta_row = move.end_row - move.start_row
        delta_col = move.end_col - move.start_col

        # frames_per_square = max(17 + -2 * abs(delta_row) + -2 * abs(delta_row), 3)
        frames_per_square = 15  # frames to move one square

        frame_count = (abs(delta_row) + abs(delta_col)) * frames_per_square

        for frame in range(frame_count + 1):
            r, c = (move.start_row + delta_row * frame / frame_count, move.start_col + delta_col * frame / frame_count)
            self._draw_board()
            self._draw_pieces(game_state.board)
            # erase the piece from its ending square
            color = pygame.Color("white") if (move.end_row + move.end_col) % 2 == 0 else pygame.Color("light blue")
            end_square = pygame.Rect(move.end_col * self.settings["SQ_SIZE"], move.end_row * self.settings["SQ_SIZE"],
                                     self.settings["SQ_SIZE"], self.settings["SQ_SIZE"])
            pygame.draw.rect(self.screen, color, end_square)
            # draw captured piece back
            if str(move.piece_captured) != "--":
                if move.is_enpassant_move:
                    captured_pawn_square = (move.start_row, move.end_col)  # The square of the captured pawn
                    captured_piece_type = game_state.board[captured_pawn_square[0]][captured_pawn_square[1]].get_type()
                    if captured_piece_type in self.settings["IMAGES"]:
                        self.screen.blit(self.settings["IMAGES"][captured_piece_type],
                                         pygame.Rect(captured_pawn_square[1] * self.settings["SQ_SIZE"],
                                                     captured_pawn_square[0] * self.settings["SQ_SIZE"],
                                                     self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))
                else:
                    self.screen.blit(self.settings["IMAGES"][move.piece_captured.get_type()], end_square)

            # print(self.settings["IMAGES"])
            # draw moving piece

            if str(move.piece_moved) != "--":

                self.screen.blit(self.settings["IMAGES"][move.piece_moved.get_type()],
                                    pygame.Rect(int(c * self.settings["SQ_SIZE"]), int(r * self.settings["SQ_SIZE"]),
                                                 self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))

            # check for castling move
            if move.is_castle_move:

                # identify the side of the castle
                if move.start_col < move.end_col:  # right side castle
                    rook_location = (7, 7) if move.piece_moved.is_white else (0, 0)
                    delta_rook_row = 0
                    delta_rook_col = -2

                    frame_count_castle = (abs(delta_rook_row) + abs(delta_rook_col)) * frames_per_square

                    r_rook, c_rook = (rook_location[0] + delta_rook_row * frame / frame_count_castle,
                                      rook_location[1] + delta_rook_col * frame / frame_count_castle)

                    rook_piece = game_state.board[rook_location[0]][rook_location[1]]

                    if str(rook_piece) != "--":
                        self.screen.blit(self.settings["IMAGES"][rook_piece.get_type()],
                                         pygame.Rect(int(c_rook * self.settings["SQ_SIZE"]),
                                                     int(r_rook * self.settings["SQ_SIZE"]),
                                                     self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))

                else:  # left side castle
                    rook_location = (7, 0) if move.piece_moved.is_white else (0, 7)
                    delta_rook_row = 0
                    delta_rook_col = 3

                    frame_count_castle = (abs(delta_rook_row) + abs(delta_rook_col)) * frames_per_square

                    r_rook, c_rook = (rook_location[0] + delta_rook_row * frame / frame_count_castle,
                                      rook_location[1] + delta_rook_col * frame / frame_count_castle)

                    rook_piece = game_state.board[rook_location[0]][rook_location[1]]

                    if str(rook_piece) != "--":
                        self.screen.blit(self.settings["IMAGES"][rook_piece.get_type()],
                                         pygame.Rect(int(c_rook * self.settings["SQ_SIZE"]),
                                                     int(r_rook * self.settings["SQ_SIZE"]),
                                                     self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))

            pygame.display.flip()
            self.clock.tick(60)

        # play relevant sounds # ToDo: Audio Fix needed
        if game_state.is_checkmate:
            self._play_sound("game_end")

        elif game_state.in_check:
            self._play_sound("check")

        elif move.is_capture:
            self._play_sound("capture")

        else:
            self._play_sound("move")

    def draw_text(self, text):
        """
        A function that draws text onto the screen
        """
        font = pygame.font.SysFont("Helvitca", 32, True, False)
        text_object = font.render(text, 0, pygame.Color("Black"))
        text_location = pygame.Rect(0, 0, gui_settings["WIDTH"], gui_settings["HEIGHT"]).move(
            gui_settings["WIDTH"] / 2 - text_object.get_width() / 2,
            gui_settings["HEIGHT"] / 2 - text_object.get_height() / 2)
        self.screen.blit(text_object, text_location)
        text_object = font.render(text, 0, pygame.Color("Gray"))
        self.screen.blit(text_object, text_location.move(2, 2))

    def _play_sound(self, sound_name):
        """
        A function that plays a sound.
        """
        self.settings["SOUNDS"][sound_name].play()


if __name__ == '__main__':

    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'Engine.Move', 'Logic.pieces', 'Game.settings'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
