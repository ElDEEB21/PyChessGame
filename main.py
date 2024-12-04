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
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # Append for both 1st and 2nd clicks
                if len(playerClicks) == 2: # After the 2nd click
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves: 
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () # Reset user clicks
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("lightblue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
def drawGameState(screen, gs):
    drawBoard(screen) 
    drawPieces(screen, gs.board)


if __name__ == "__main__":
    main()