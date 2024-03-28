from __future__ import annotations

import copy
from ChessEngine.Move import Move
from ChessEngine.GameState import GameState
from SmartMoveFinder.Settings import tree_settings
from SmartMoveFinder.BoardAlgorithems import board_evaluation


class MovesFinderTree:
    _move: Move | None
    _next_logical_moves: list[MovesFinderTree]
    is_whites_turn: bool

    def __init__(self, game_state: GameState, white_to_move: bool, move: Move = None, depth: int = tree_settings["DEPTH"]):
        print("MovesFinderTree init")
        self._move = move
        self._next_logical_moves = []
        self.is_whites_turn = white_to_move

        # create the rest
        self.add_next_possible_move(game_state, depth)
        print("MovesFinderTree init done")

    def add_next_possible_move(self, game_state: GameState, current_depth: int = 0):
        if current_depth == 0:
            return
        print(current_depth)

        for move in game_state.get_valid_moves():
            self._next_logical_moves.append(MovesFinderTree(game_state, not self.is_whites_turn, move, 0))

        else:
            for move in self._next_logical_moves:
                move.add_next_possible_move(game_state, current_depth - 1)

    def is_master_root(self):
        return self._move is None

    def is_leaf(self):
        return len(self._next_logical_moves) == 0

    def find_best_move(self, game_state: GameState) -> int | Move:

        if self.is_leaf():
            game_state_new = copy.copy(game_state)
            game_state_new.make_move(self._move)

            # score = board_evaluation(game_state_new)

            return board_evaluation(game_state_new)

        elif self.is_master_root():
            best_score, best_move = -1000, None
            for move in self._next_logical_moves:
                print(game_state)
                game_state.make_move(move._move)

                score = move.find_best_move(game_state)

                if score > best_score:
                    best_score = score
                    best_move = move._move

                game_state.undo_move()

            return best_move

        else:
            best_score, best_move = -1000, None
            for move in self._next_logical_moves:
                game_state.make_move(move._move)

                score = move.find_best_move(game_state)

                if score > best_score:
                    best_score = score
                    best_move = move._move

                game_state.undo_move()

            return best_score


