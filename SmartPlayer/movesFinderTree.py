from __future__ import annotations

import copy

from Engine import Move, GameState
from .boardAlgorithms import board_evaluation
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
            self._is_whites_move = False
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

    def find_next_best_move(self, game_state):

        print(game_state.white_to_move, self._is_whites_move)

        print(self._is_whites_move == game_state.white_to_move)

        # Assert statement
        assert self._is_whites_move is not game_state.white_to_move

        # Actual recursive code
        if self.is_leaf():
            return board_evaluation(game_state)  # Compute board_evaluation algorithm

        elif self.is_root():
            best_move, max_score = None, -1000
            copy_of_game_state = copy.copy(game_state)

            for next_possible_move in self._next_valid_moves:

                copy_of_game_state.make_move(next_possible_move._move)
                print("after_move: ", copy_of_game_state.white_to_move)

                score = next_possible_move.find_next_bast_move(copy_of_game_state)

                if score > max_score:
                    max_score, best_move = score, next_possible_move._move

                copy_of_game_state.undo_move()

            return best_move

        else:
            best_move, max_score = None, -1000
            copy_of_game_state = copy.copy(game_state)

            for next_possible_move in self._next_valid_moves:

                copy_of_game_state.make_move(next_possible_move._move)

                score = next_possible_move.find_next_bast_move(copy_of_game_state)

                if score > max_score:
                    max_score = score

                copy_of_game_state.undo_move()

            return max_score


    def print_tree(self, indent=0):
        print(' ' * indent + str(self._move), self._is_whites_move)
        for child in self._next_valid_moves:
            child.print_tree(indent + 2)



if __name__ == '__main__':
    tree = MoveFinderTree(game_state=GameState())
    tree.print_tree()





