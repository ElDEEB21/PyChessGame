# PyChessGame

PyChessGame is a simple chess game implemented in Python. This project includes a graphical user interface (GUI) for playing chess, as well as an AI opponent that can make moves based on different algorithms.

## Project Structure

The project is divided into several files and folders, each responsible for different aspects of the game:

### Files


#### 1. [`main.py`](main.py)

This file contains the `ChessGame` class, which is responsible for the main game loop and handling user interactions. It initializes the game, loads images, handles mouse clicks and key presses, and updates the game state. It also includes methods for drawing the game board, pieces, and sidebar, as well as displaying end-game messages and promotion choices.

- **`ChessGame` Class**: This class manages the overall game, including the GUI and user interactions.
  - **Attributes**:
    - `screen`: The Pygame screen object.
    - `clock`: The Pygame clock object.
    - `gs`: The current game state.
    - `validMoves`: A list of valid moves for the current game state.
    - `moveMade`: A boolean indicating if a move has been made.
    - `sqSelected`: The currently selected square.
    - `playerClicks`: A list of player clicks.
    - `selectedPieceMoves`: A list of valid moves for the selected piece.
    - `capturedPieces`: A dictionary of captured pieces for both players.
    - `playerOne`: A boolean indicating if player one is a human.
    - `playerTwo`: A boolean indicating if player two is a human.
  - **Methods**:
    - `loadImages`: Loads the images for the chess pieces.
    - `initializeGame`: Initializes the game, including setting up the screen, clock, and loading images.
    - `mainLoop`: The main game loop, which handles events, updates the game state, and redraws the screen.
    - `handleMouseClick`: Handles mouse click events.
    - `handleKeyPress`: Handles key press events.
    - `showESCWindow`: Displays the settings window.
    - `handleAIMove`: Handles the AI's move.
    - `resetGame`: Resets the game state.
    - `drawGameState`: Draws the current game state.
    - `drawBoard`: Draws the chessboard.
    - `drawPieces`: Draws the chess pieces.
    - `drawSidebar`: Draws the sidebar.
    - `showStartWindow`: Displays the start window.
    - `showSettingsWindow`: Displays the settings window.
    - `handleDifficultyChange`: Handles changes to the AI difficulty.
    - `handleMuteToggle`: Toggles the mute setting.
    - `showColorChoiceWindow`: Displays the color choice window.
    - `showPromotionChoices`: Displays the promotion choices.
    - `showEndGameMessage`: Displays the end game message.


#### 2. [`engine.py`](engine.py)

This file contains the `GameState` class, which inherits from `MoveGenerator`. It maintains the current state of the game, including the board, move log, castling rights, and en passant possibilities. It includes methods for making and undoing moves, checking for pins and checks, and determining valid moves. It also handles special rules like the fifty-move rule, threefold repetition, and insufficient material.

- **`GameState` Class**: This class represents the current state of the chess game.
  - **Attributes**:
    - `board`: A 2D list representing the chessboard.
    - `moveFunctions`: A dictionary mapping piece types to their move generation functions.
    - `whiteToMove`: A boolean indicating if it is white's turn to move.
    - `moveLog`: A list of moves made in the game.
    - `whiteKingLocation`: The current location of the white king.
    - `blackKingLocation`: The current location of the black king.
    - `inCheck`: A boolean indicating if the current player is in check.
    - `checkmate`: A boolean indicating if the game is in checkmate.
    - `stalemate`: A boolean indicating if the game is in stalemate.
    - `pins`: A list of pinned pieces.
    - `checks`: A list of checks.
    - `enpassantPossible`: The coordinates for en passant capture.
    - `currentCastleRights`: The current castling rights.
    - `castleRightsLog`: A log of castling rights.
    - `fiftyMoveCounter`: A counter for the fifty-move rule.
  - **Methods**:
    - `makeMove`: Makes a move on the board.
    - `undoMove`: Undoes the last move.
    - `updateCastleRights`: Updates the castling rights after a move.
    - `getValidMoves`: Returns a list of valid moves for the current game state.
    - `getAllPossibleMoves`: Returns a list of all possible moves for the current game state.
    - `checkForPinsAndChecks`: Checks for pins and checks.
    - `squareUnderAttack`: Checks if a square is under attack.
    - `insufficientMaterial`: Checks for insufficient material to continue the game.


#### 3. [`moves.py`](moves.py)

This file contains the `MoveGenerator` class, which is responsible for generating all possible moves for each piece on the chessboard. It includes methods for generating moves for pawns, rooks, knights, bishops, queens, and kings. It also handles special moves like castling and en passant.

- **`MoveGenerator` Class**: This class contains methods to generate all possible moves for each type of piece on the chessboard.
  - **`getPawnMoves` Method**: Generates all possible moves for a pawn located at a given position. It handles normal moves, captures, en passant, and promotions.
  - **`getRookMoves` Method**: Generates all possible moves for a rook located at a given position. It handles horizontal and vertical moves.
  - **`getKnightMoves` Method**: Generates all possible moves for a knight located at a given position. It handles L-shaped moves.
  - **`getBishopMoves` Method**: Generates all possible moves for a bishop located at a given position. It handles diagonal moves.
  - **`getQueenMoves` Method**: Generates all possible moves for a queen located at a given position. It combines the moves of a rook and a bishop.
  - **`getKingMoves` Method**: Generates all possible moves for a king located at a given position. It handles one-square moves in any direction and castling.
  - **`getCastleMoves` Method**: Generates all possible castling moves for a king located at a given position.
  - **`getKingsideCastleMoves` Method**: Generates kingside castling moves.
  - **`getQueensideCastleMoves` Method**: Generates queenside castling moves.

- **`CastleRights` Class**: This class represents the castling rights for both players.
  - **Attributes**:
    - `wks`: White king-side castling right.
    - `bks`: Black king-side castling right.
    - `wqs`: White queen-side castling right.
    - `bqs`: Black queen-side castling right.

- **`Move` Class**: This class represents a chess move.
  - **Attributes**:
    - `startSq`: The starting square of the move.
    - `endSq`: The ending square of the move.
    - `board`: The current state of the board.
    - `isEnpassantMove`: A boolean indicating if the move is an en passant capture.
    - `isCastleMove`: A boolean indicating if the move is a castling move.
  - **Methods**:
    - `__eq__`: Checks if two moves are equal.
    - `getRankFile`: Converts a row and column to a rank and file.
    - `getChessNotation`: Returns the chess notation for the move.

#### 4. [`computer.py`](computer.py)

This file contains functions for the AI opponent. It includes different algorithms for finding the best move, such as Minimax, Negamax, and Alpha-Beta pruning. It also includes a simple function for finding a random move. The AI evaluates the board based on material score and can handle checkmate and stalemate situations.

- **Functions**:
  - `findRandomMove`: Returns a random move from the list of valid moves.
  - `findBestMoveAlphaBeta`: Finds the best move using the Alpha-Beta pruning algorithm.
  - `alphaBeta`: The Alpha-Beta pruning algorithm.
  - `scoreBoard`: Evaluates the board and returns a score.
  - `scoreMaterial`: Scores the board based on material.

### Folders

#### 1. [`images/`](images)

This folder contains all the image assets used in the game, such as the chess pieces and the board. These images are loaded in `main.py` to be displayed in the GUI.

#### 2. [`sounds/`](sounds)

This folder contains sound effects used in the game, such as move sounds and game end sounds. These sounds enhance the user experience by providing audio feedback for actions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ElDEEB21/PyChessGame.git
    ```
2. Navigate to the project directory:
    ```bash
    cd PyChessGame
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Dependencies

- Python 3.x
- Pygame

## How to Run

1. Ensure you have Python installed on your system.
2. Install the required dependencies (e.g., Pygame).
3. Run the `main.py` file to start the game.

```bash
python main.py
```

## Features

- Play against another human or an AI opponent.
- Choose from different AI difficulty levels.
- Save and load game states.
- Undo and redo moves.
- View move history.
- Customize board and piece colors.
- Toggle sound effects on and off.


## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.


## Acknowledgements

- The Pygame community for their excellent resources and support.
- The contributors who helped improve this project.

## Contact

For any questions or feedback, please contact ar2724@fayoum.edu.eg.
