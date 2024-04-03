# from ChessMain.ChessMain import main
from Game.game import main
from SmartPlayer import MoveFinderTree, Engine
from Logic import GameState



def run():
    # from Game import game
    main()
    # game_state = GameState()
    # engine = Engine(game_state)
    # print(engine.tree.get_depth())
    
    # for i in range(2):
    #     next_move = engine.find_best_move_tree(game_state, game_state.get_valid_moves_advanced())
        
    #     print("Move Made: ", next_move)
    #     game_state.make_move(next_move)
        
    #     print("Current Depth", engine.tree.get_depth())








if __name__ == '__main__':
    run()
