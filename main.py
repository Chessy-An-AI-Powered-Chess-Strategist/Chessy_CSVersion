# from ChessMain.ChessMain import main
from Game.game import main
from SmartPlayer import MoveFinderTree
from Engine.gameState import GameState


def run():
    # from Game import game
    main()
    # game_state = GameState()
    # print(type(game_state))
    # tree = MoveFinderTree(game_state, None)
    # tree.print_tree()

if __name__ == '__main__':
    run()
