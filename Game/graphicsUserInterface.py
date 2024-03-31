import pygame
from Engine.Move import Move


class GraphicsUserInterface:
    """
    This class is responsible for the graphics of the game.
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
                pygame.draw.rect(self.screen, color, pygame.Rect(c * self.settings["SQ_SIZE"], r * self.settings["SQ_SIZE"], self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))

    def _draw_pieces(self, board):
        """
        A function that draws the pieces on the screen.
        """
        for r in range(self.settings["DIMENSION"]):
            for c in range(self.settings["DIMENSION"]):
                piece = board[r][c]
                if piece != "--":
                    self.screen.blit(self.settings["IMAGES"][piece],
                                pygame.Rect(c * self.settings["SQ_SIZE"], r * self.settings["SQ_SIZE"],
                                       self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))

    def _highlight_squares(self, game_state):
        if self.sq_selected != ():
            r, c = self.sq_selected[0], self.sq_selected[1]
            if game_state.board[r][c][0] == ("w" if game_state.white_to_move else "b"):  # sq_selected is a piece that can be moved
                s = pygame.Surface((self.settings["SQ_SIZE"], self.settings["SQ_SIZE"]))
                s.set_alpha(100)  # transparency value
                s.fill(pygame.Color("blue"))
                self.screen.blit(s, (c * self.settings["SQ_SIZE"], r * self.settings["SQ_SIZE"]))
                s.fill(pygame.Color("yellow"))
                for move in game_state.get_valid_moves_video():
                    if move.start_row == r and move.start_col == c:
                        self.screen.blit(s, (move.end_col * self.settings["SQ_SIZE"], move.end_row * self.settings["SQ_SIZE"]))

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
                else:
                    # select
                    self.sq_selected = (row, col)
                    self.player_clicks.append(self.sq_selected)

                # Check if the player has clicked twice to make a move
                if len(self.player_clicks) == 2:
                    self.make_move(game_state, Move(self.player_clicks[0], self.player_clicks[1], game_state.board))

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    self._undo_move(game_state)

        return True  # Tell running to continue

    def make_move(self, game_state, move_object):
        """
        A function that makes a move in the game.
        """
        self.valid_moves = game_state.get_valid_moves_video()

        # print(move_object)
        for i in range(len(self.valid_moves)):
            if move_object == self.valid_moves[i]:
                move_object.is_capture = self.valid_moves[i].is_capture

                game_state.make_move(self.valid_moves[i])

                # play the move sound # ToDo: Sound does not work
                # if game_state.is_checkmate:
                #     self._play_sound("game_end")
                #
                # elif game_state.in_check:
                #     self._play_sound("check")
                #
                # elif self.valid_moves[i].is_capture:
                #     self._play_sound("capture")
                #
                # else:
                #     self._play_sound("move")

                # animate move
                self._animate_move(game_state, self.valid_moves[i])

                # display the move
                self.draw_game_state(game_state)

        # reset the player clicks
        self.sq_selected = ()
        self.player_clicks = []

    def _undo_move(self, game_state):
        """
        A function that undoes a move in the game.
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
        frames_per_square = 15 # frames to move one square

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
            if move.piece_captured != "--":
                self.screen.blit(self.settings["IMAGES"][move.piece_captured], end_square)
            # draw moving piece
            self.screen.blit(self.settings["IMAGES"][move.piece_moved],
                        pygame.Rect(int(c * self.settings["SQ_SIZE"]), int(r * self.settings["SQ_SIZE"]),
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

    def _play_sound(self, sound_name):
        """
        A function that plays a sound.
        """
        self.settings["SOUNDS"][sound_name].play()










