from __future__ import annotations

import copy

from Engine import Move, GameState
from .settings import tree_settings


class MoveFinderTree:
    _move: Move or None
    _next_valid_moves: list[MoveFinderTree]
    _is_whites_move: bool

    def __init__(self, game_state: GameState, move: Move = None):

        self._move = move
        self._next_valid_moves = []
        self._is_whites_move = game_state.white_to_move

        if self.is_root():
            for _ in range(tree_settings["DEPTH"]):
                # create the rest
                self.add_next_possible_moves(game_state)

    def is_root(self):
        return self._move is None

    def is_leaf(self):
        return self._next_valid_moves == []

    def add_next_possible_moves(self, game_state: GameState):

        if self.is_leaf():

            for next_possible_move in game_state.get_valid_moves():
                self._next_valid_moves.append(MoveFinderTree(game_state, next_possible_move))

        else:
            for move in self._next_valid_moves:
                copy_of_game_state = copy.copy(game_state)
                copy_of_game_state.make_move(move._move)
                move.add_next_possible_moves(copy_of_game_state)

    def print_tree(self, indent=0):
        print(' ' * indent + str(self._move), self._is_whites_move)
        for child in self._next_valid_moves:
            child.print_tree(indent + 2)



if __name__ == '__main__':
    tree = MoveFinderTree(game_state=GameState())
    tree.print_tree()





