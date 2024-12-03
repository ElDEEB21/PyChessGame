import pygame as p
import engine

WIDTH = HEIGHT = 512
DIMENSION = 8 # Chess board is 8x8
SQ_SIZE = HEIGHT
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
    gs = engine.GameState()
    loadImages()
    running = True
    sqSelected = () # No square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # Keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # The user clicked the same square twice
                    sqSelected = () # Deselect
                    playerClicks = [] # Clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # Append for both 1st and 2nd clicks
                if len(playerClicks) == 2: # After the 2nd click
                    move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    gs.makeMove(move)
                    sqSelected = () # Reset user clicks
                    playerClicks = []
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