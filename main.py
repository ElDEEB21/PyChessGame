import pygame as p
from engine import GameState
from moves import MoveGenerator, Move

WIDTH = HEIGHT = 512
DIMENSION = 8 # Chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # For animations later on
IMAGES = {}

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    p.display.set_caption("Chess Game")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = () # tuple: (row, col)
    playerClicks = [] # Keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    selectedPieceMoves = [] # Store valid moves for the selected piece
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # location of the mouse (x, y)
                col, row = (location[0] // SQ_SIZE), (location[1] // SQ_SIZE)
                if sqSelected == (row, col): # The user clicked the same square twice
                    sqSelected = () # Deselect
                    playerClicks = [] # Clear player clicks
                    selectedPieceMoves = [] # Clear valid moves for the selected piece
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # Append for both 1st and 2nd clicks
                    selectedPieceMoves = [move for move in validMoves if move.startRow == row and move.startCol == col]
                if len(playerClicks) == 2: # After the 2nd click
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]: 
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () # Reset user clicks
                            playerClicks = []
                            selectedPieceMoves = [] # Clear valid moves for the selected piece
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                
        drawGameState(screen, gs, sqSelected, selectedPieceMoves)
        
        if gs.checkmate:
            showEndGameMessage(screen, "Checkmate")
            running = False
        elif gs.stalemate:
            showEndGameMessage(screen, "Stalemate")
            running = False

        clock.tick(MAX_FPS)
        p.display.flip()

def drawBoard(screen, gs, sqSelected, selectedPieceMoves):
    colors = [p.Color("white"), p.Color("lightblue")]
    selectedColor = p.Color("yellow")  # Color for the selected square
    moveColor = p.Color("green")  # Color for valid move squares
    checkColor = p.Color("red")  # Color for the king in check
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if sqSelected == (r, c):  # Check if this square is selected
                color = selectedColor
            elif (r, c) in [(move.endRow, move.endCol) for move in selectedPieceMoves]:  # Check if this square is a valid move
                color = moveColor
            else:
                color = colors[((r + c) % 2)]
            # ----------------------------------------------------------------------------------------------------------
            # Check Color
            if gs.inCheck and ((gs.whiteToMove and (r, c) == gs.whiteKingLocation) or 
                               (not gs.whiteToMove and (r, c) == gs.blackKingLocation)):
                color = checkColor
            # Check Sound
            if gs.inCheck and not hasattr(gs, 'checkSoundPlayed'):
                p.mixer.Sound('sounds/move-check.mp3').play()
                gs.checkSoundPlayed = True
            elif not gs.inCheck:
                if hasattr(gs, 'checkSoundPlayed'):
                    del gs.checkSoundPlayed
            # Checkmate Sound
            if gs.checkmate and not hasattr(gs, 'checkmateSoundPlayed'):
                p.mixer.Sound('sounds/chess_com_checkmate.mp3').play()
                gs.checkmateSoundPlayed = True
            elif not gs.checkmate:
                if hasattr(gs, 'checkmateSoundPlayed'):
                    del gs.checkmateSoundPlayed
            # ----------------------------------------------------------------------------------------------------------
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
def drawGameState(screen, gs, sqSelected, selectedPieceMoves):
    drawBoard(screen, gs, sqSelected, selectedPieceMoves)  # Pass the selected square and valid moves to the drawBoard function
    drawPieces(screen, gs.board)

def showEndGameMessage(screen, message):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(message, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - textObject.get_width() // 2, HEIGHT // 2 - textObject.get_height() // 2)
    screen.blit(textObject, textLocation)
    p.display.flip()
    p.time.wait(3000)

if __name__ == "__main__":
    main()