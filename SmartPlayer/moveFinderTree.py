from __future__ import annotations

import copy
import networkx as nx
from plotly.graph_objs import Scatter, Figure

from Logic import Move, GameState
from .boardAlgorithms import board_evaluation
import random


class MoveFinderTree:
    """
    A tree structure to find the best move
    """
    move: Move or None
    next_valid_moves: list[MoveFinderTree]
    _is_whites_move: bool

    def __init__(self, game_state: GameState, move: Move = None):

        self.move = move
        self.next_valid_moves = []
        self._is_whites_move = game_state.white_to_move

    def is_root(self):
        """
        Check if the tree is the root
        """
        return not isinstance(self.move, Move)

    def is_leaf(self):
        """
        Check if the tree is a leaf
        """
        return len(self.next_valid_moves) == 0

    def get_depth(self):
        """
        Get the depth of the tree
        """
        if self.is_leaf():
            return 0
        else:
            return max([next_possible_move.get_depth() for next_possible_move in self._next_valid_moves] + [0]) + 1

    def add_next_possible_moves(self, game_state: GameState):

        copy_of_game_state = copy.deepcopy(game_state)

        if self.is_leaf():
            for next_possible_move in copy_of_game_state.get_valid_moves_advanced():
                self.next_valid_moves.append(MoveFinderTree(copy_of_game_state, next_possible_move))
        else:
            for move in self.next_valid_moves:
                copy_of_game_state.make_move(move.move)

                move.add_next_possible_moves(copy_of_game_state)

                copy_of_game_state.undo_move()

    def find_next_best_move(self, game_state: GameState) -> Move:
        copy_of_game_state = copy.deepcopy(game_state)
        turn_multiplier = 1 if game_state.white_to_move else -1

        best_move, score = self.find_move_negamax(copy_of_game_state, turn_multiplier)
        return best_move

    def find_move_negamax(self, game_state: GameState, turn_multiplier) -> (Move, int):
        next_move = None
        max_score = -1000  # - checkmate

        if self.is_leaf():
            return None, turn_multiplier * board_evaluation(game_state)

        else:
            random.shuffle(self.next_valid_moves)
            for move in self.next_valid_moves:
                game_state.make_move(move.move)
                score = -move.find_move_negamax(game_state, -turn_multiplier)[1]

                if score > max_score:
                    max_score = score
                    next_move = self.move

                    if self.is_root():
                        next_move = move.move

                game_state.undo_move()

            return next_move, max_score

    def print_tree(self, indent=0):
        print(' ' * indent + str(self.move), self._is_whites_move)
        for child in self._next_valid_moves:
            child.print_tree(indent + 2)

    def draw_tree(self):
        G = nx.DiGraph()
        labels = {}


        def add_edges(node, parent=None):
            labels[str(node.move)] = str(node.move)
            if parent is not None:
                G.add_edge(id(parent), id(node))
            for child in node._next_valid_moves:
                add_edges(child, node)

        add_edges(self)

        pos = nx.spring_layout(G)
        x_values = [pos[k][0] for k in G.nodes]
        y_values = [pos[k][1] for k in G.nodes]

        x_edges = []
        y_edges = []

        for edge in G.edges:
            x1, x2 = pos[edge[0]][0], pos[edge[1]][0]
            x_edges += [x1, x2, None]
            y1, y2 = pos[edge[0]][1], pos[edge[1]][1]
            y_edges += [y1, y2, None]

        trace3 = Scatter(x=x_edges,
                         y=y_edges,
                         mode='lines',
                         line=dict(color='rgb(210,210,210)', width=1),
                         )

        trace4 = Scatter(x=x_values,
                         y=y_values,
                         mode='markers',
                         marker=dict(symbol='circle-dot',
                                     size=5,
                                     color='#2E91E5',
                                     line=dict(color='rgb(50, 50, 50)', width=0.5)
                                     ),
                         text=list(G.nodes),
                         hovertemplate='%{text}',
                         hoverlabel={'namelength': 0}
                         )

        fig = Figure(data=[trace3, trace4])
        fig.update_layout({'showlegend': False})
        fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
        fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
        fig.show()

    def move_down(self, move: Move):
        """move down the tree"""
        for node in self.next_valid_moves:
            if node.move.move_id == move.move_id:
                self.next_valid_moves = node.next_valid_moves
                self._is_whites_move = node._is_whites_move

                break
