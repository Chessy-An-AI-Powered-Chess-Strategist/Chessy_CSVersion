# Chessy

## Group Members:
- Ali Rahbar (Student Number: 1010207964)
- ...
- ...
- ...

# Project Overview:

Chessy is a fully implimented software created for users to play chess with friends or with bots. This project is being codded for our CSC111 class to show our understanding and mastery in the course content. 

### Objecttive:
To develop a chess engine that utilizes a tree structure to map out possible moves ahead (e.g., depth 4 for four moves ahead) and uses an algorithm to evaluate each move based on board positioning and piece values. 

### Scope:

1. Graphics User Interface: This is what you see on the screen when you play. It's where the chessboard and pieces are displayed, and where you make your moves.
2. Chess Logic Folder: Inside this folder, we wrote the code that controls how the game works. It's like the brain behind the game, making sure the pieces move correctly and following all the rules.
3. Bot Chess Player: We also made a computer player you can play against. It's like having a virtual opponent when you want to practice on your own.


# Resources Used:
## Knoledge based resources:
- Chess engine article from Cornell University: https://www.cs.cornell.edu/boom/2004sp/ProjectArch/Chess/algorithms.html
- Chess Engine in Python by Eddie Sharick: https://youtu.be/EnYui0e73Rs?si=PV5_Up-VEutjJb9Q
- Graphics (Open source) : https://opengameart.org/content/madwares-chess-set
- Note: There where no datasets used in this project. The data that the tree works with is dynamically generated as the game progresses to save memory and make program more efficient.
## Developer tools:
- OpenAI's Chat GPT (Helped with writing comments and reports)
- Github Copilot (Develppers coding assistant)
- Github (Teams version control system)
- Jetbrains Qodana (Analize software vanerabilities)

# Timeline (3 Weeks)

## Week 1: Setup and Initial Development
- Setup project environment using the python chess library(temporarly)
- Start developing the tree structure for mapping moves.
## Week 2: Setup software arcitecture and create user interface
- Develop and test the evaluation algorithm.
- Created the User interface
- Integrated the UI with basic tree and fix comoatibilaty issues
## Week 3: Develop chess logic and minimax algorithms
- Develop the logic for each piece in the game
- Impliment the minimax algorithm so the bots can play instead of players

# How to run program:
1. Intall the required packages int eh requirements.txt file:
   ```python pip install -r requirements.txt```

2. Choose the mode you like to play in the `game/game.py` file:
   - If you wish to play player vs player:
   ```css
       # define player states
       is_player_white_human = True
       is_player_black_human = True
   ```
   Note: Only in the player vs player mode you can undo a move by pressing the button z.
   - If you wish to see the bots play against each other:
    ```css
      # define player states
      is_player_white_human = False
      is_player_black_human = False
    ```

3. Run the `main.py` file in the directory and the code will start working

# About Software:

## Data Flow Diagram:
The follwoing is the software arcitecture and how each module communicates with one another in the code and what data they transfer to one another
# ToDo

## Algorithms:
In this project we where required to develop and impliment many advanced algorithms. Here are a list of the main ones:
1. The Negamax Algorithm: This algorithm is the advanced version of minimax that we have used in the tree to go thoruhg all the possibilities, minimize the oponens score and maximize its own score. The Negamax algorithm playes the core part of the decision making process of the chess bots.
2. The king is check algorithm: This algorithm checks the kings position and weather or not the king is in check. The problem with this algorithm was its efficiency as it was being called multiple times in each turn.
3. Pieces get move algorithms: Each move on the chess board also had a get moves method which would generate the possible moves that algorithm could make. All pieces in the code inheriete properties from the `chess_piece` class which has a not implimented method called `get_moves`. All the poiueces on the bord impliment this method with their own special algorithm with generates how they can move. coding these was also a major challange of the project.

## Graphics:
The graphics of the game was also implimented using a layered structure where smaller methods each generate a layer of content on top of each other to geenrate the userfriendly easy to use interface. The layers are as follows from the top to bottom:

1. Displayed text 
2. Chess pieces
3. Movement highloights
4. Board graphics

This structure allowed us to create a smooth and dynamic user experiecne as everytime the page would update only the related section would change making in more efficient. Not that the order the layers where gerated where from number 4 to 1.



# Chenges we made:

# Project refelection:



