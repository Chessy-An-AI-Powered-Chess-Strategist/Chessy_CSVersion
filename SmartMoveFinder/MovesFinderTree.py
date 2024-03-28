from ChessEngine.Move import Move
from ChessEngine.GameState import GameState
from SmartMoveFinder.Settings import tree_settings


class MovesFinderTree:
    _move: Move | None
    _next_logical_moves: list[Move]
    is_whites_turn: bool

    def __init__(self, game_state: GameState, move:Move = None):
        self._move = move
        self._next_logical_moves = []
        self.is_whites_turn = game_state.white_to_move

        # create the rest
        self.add_next_possible_move(game_state, tree_settings["DEPTH"])

    def add_next_possible_move(self, game_state: GameState, current_depth: int = 0):

        for move in game_state.get_valid_moves():
            self._next_logical_moves.append(move)

        if current_depth > 0:
            self.add_next_possible_move(game_state, current_depth - 1)






