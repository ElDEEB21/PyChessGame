import pygame as p
from engine import GameState
from moves import MoveGenerator, Move

WIDTH = HEIGHT = 512
SIDEBAR_WIDTH = 200
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
    screen = p.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))
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
    capturedPieces = {"w": [], "b": []} # Store captured pieces

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # location of the mouse (x, y)
                if location[0] < WIDTH: # Click on the board
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
                                if move.pieceCaptured != "--":
                                    capturedPieces[move.pieceCaptured[0]].append(move.pieceCaptured)
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                
        drawGameState(screen, gs, sqSelected, selectedPieceMoves, capturedPieces)
        
        if gs.checkmate:
            showEndGameMessage(screen, "Checkmate", "Black" if gs.whiteToMove else "White")
            running = False
        elif gs.stalemate:
            showEndGameMessage(screen, "Stalemate", None)
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

def drawSidebar(screen, gs, capturedPieces):
    # Draw the sidebar background
    sidebarRect = p.Rect(WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    p.draw.rect(screen, p.Color("gray"), sidebarRect)
    
    # Set up font
    font = p.font.SysFont("Helvetica", 24, True, False)
    
    # Display whose turn it is using color
    turnColor = p.Color("white") if gs.whiteToMove else p.Color("black")
    turnRect = p.Rect(WIDTH + 10, 10, 30, 30)
    p.draw.rect(screen, turnColor, turnRect)
    
    # Display captured pieces
    yOffset = 60
    pieceSize = SQ_SIZE // 2  # Smaller size for captured pieces
    for color, pieces in capturedPieces.items():
        colorText = "White captured:" if color == "w" else "Black captured:"
        colorObject = font.render(colorText, 0, p.Color("Black"))
        screen.blit(colorObject, (WIDTH + 10, yOffset))
        yOffset += 30
        for piece in pieces:
            pieceImage = p.transform.scale(IMAGES[piece], (pieceSize, pieceSize))
            screen.blit(pieceImage, (WIDTH + 10, yOffset))
            yOffset += pieceSize + 5  # Add some space between pieces

def drawGameState(screen, gs, sqSelected, selectedPieceMoves, capturedPieces):
    drawBoard(screen, gs, sqSelected, selectedPieceMoves)  # Pass the selected square and valid moves to the drawBoard function
    drawPieces(screen, gs.board)
    drawSidebar(screen, gs, capturedPieces)

def showEndGameMessage(screen, message, winner):
    font = p.font.SysFont("Helvetica", 32, True, False)
    if winner:
        message = f"{winner} wins by {message}"
    textObject = font.render(message, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - textObject.get_width() // 2, HEIGHT // 2 - textObject.get_height() // 2)
    screen.blit(textObject, textLocation)
    
    # Draw buttons
    playAgainButton = p.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    quitButton = p.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
    p.draw.rect(screen, p.Color("green"), playAgainButton)
    p.draw.rect(screen, p.Color("red"), quitButton)
    
    playAgainText = font.render("Play Again", 0, p.Color("Black"))
    quitText = font.render("Quit", 0, p.Color("Black"))
    screen.blit(playAgainText, playAgainButton.move(50, 10))
    screen.blit(quitText, quitButton.move(75, 10))
    
    p.display.flip()
    
    waiting = True
    while waiting:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if playAgainButton.collidepoint(location):
                    main()
                    waiting = False
                elif quitButton.collidepoint(location):
                    p.quit()
                    exit()

if __name__ == "__main__":
    main()