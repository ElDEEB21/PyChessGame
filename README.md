# PyChessGame

PyChessGame is a simple chess game implemented in Python. This project includes a graphical user interface (GUI) for playing chess, as well as an AI opponent that can make moves based on different algorithms.

## Project Structure

The project is divided into several files and folders, each responsible for different aspects of the game:

### Files

#### 1. [`moves.py`](moves.py)

This file contains the `MoveGenerator` class, which is responsible for generating all possible moves for each piece on the chessboard. It includes methods for generating moves for pawns, rooks, knights, bishops, queens, and kings. It also handles special moves like castling and en passant.

#### 2. [`main.py`](main.py)

This file contains the `ChessGame` class, which is responsible for the main game loop and handling user interactions. It initializes the game, loads images, handles mouse clicks and key presses, and updates the game state. It also includes methods for drawing the game board, pieces, and sidebar, as well as displaying end-game messages and promotion choices.

#### 3. [`engine.py`](engine.py)

This file contains the `GameState` class, which inherits from `MoveGenerator`. It maintains the current state of the game, including the board, move log, castling rights, and en passant possibilities. It includes methods for making and undoing moves, checking for pins and checks, and determining valid moves. It also handles special rules like the fifty-move rule, threefold repetition, and insufficient material.

#### 4. [`computer.py`](computer.py)

This file contains functions for the AI opponent. It includes different algorithms for finding the best move, such as Minimax, Negamax, and Alpha-Beta pruning. It also includes a simple function for finding a random move. The AI evaluates the board based on material score and can handle checkmate and stalemate situations.

### Folders

#### 1. [`images/`](images/)

This folder contains all the image assets used in the game, such as the chess pieces and the board. These images are loaded in `main.py` to be displayed in the GUI.

#### 2. [`sounds/`](sounds/)

This folder contains sound effects used in the game, such as move sounds and game end sounds. These sounds enhance the user experience by providing audio feedback for actions.

## How to Run

1. Ensure you have Python installed on your system.
2. Install the required dependencies (e.g., Pygame).
3. Run the `main.py` file to start the game.

```bash
python main.py
```

## Features

- **Graphical User Interface**: The game includes a GUI for playing chess, with a sidebar displaying captured pieces and the current player's turn.
- **Move Generation**: The `MoveGenerator` class generates all possible moves for each piece, including special moves like castling and en passant.
- **AI Opponent**: The AI can make moves based on different algorithms, including Minimax, Negamax, and Alpha-Beta pruning.
- **Game Rules**: The game enforces all standard chess rules, including check, checkmate, stalemate, the fifty-move rule, threefold repetition, and insufficient material.
- **Sound Effects**: The game includes sound effects for moves and game end scenarios to enhance the user experience.

## Future Improvements

- **Enhance AI**: Improve the AI's evaluation function and search depth for better gameplay.
- **Add More Features**: Implement additional features like move animations, game saving/loading, and online multiplayer.
- **Improve GUI**: Enhance the graphical interface with better visuals and animations.
- **Sound Customization**: Allow users to customize sound effects and add their own.

Enjoy playing PyChessGame!