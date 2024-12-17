import pygame as p
import computer
from engine import GameState
from moves import MoveGenerator, Move

WIDTH = HEIGHT = 512
SIDEBAR_WIDTH = 200
DIMENSION = 8  # Chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For animations later on
AI_Depth = 3
isMuted = False
IMAGES = {}

class ChessGame:
    def __init__(self):
        self.screen = None
        self.clock = None
        self.gs = GameState()
        self.validMoves = self.gs.getValidMoves()
        self.moveMade = False
        self.sqSelected = None  # tuple: (row, col)
        self.playerClicks = []  # Keep track of player clicks (two tuples: [(6, 4), (4, 4)])
        self.selectedPieceMoves = []  # Store valid moves for the selected piece
        self.capturedPieces = {"w": [], "b": []}  # Store captured pieces
        self.playerOne, self.playerTwo = None, None

    def loadImages(self):
        pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    def initializeGame(self):
        p.init()
        p.display.set_caption("Chess Game")
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.clock = p.time.Clock()
        self.screen.fill(p.Color("white"))
        self.loadImages()
        self.playerOne, self.playerTwo = self.showStartWindow()
        self.screen = p.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))

    def mainLoop(self):
        running = True
        while running:
            humanTurn = (self.gs.whiteToMove and self.playerOne) or (not self.gs.whiteToMove and self.playerTwo)
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    if humanTurn:
                        self.handleMouseClick(e)
                elif e.type == p.KEYDOWN:
                    self.handleKeyPress(e)
            if not humanTurn:
                self.handleAIMove()
            if self.moveMade:
                self.validMoves = self.gs.getValidMoves()
                self.moveMade = False
            self.drawGameState()
            if self.gs.checkmate or self.gs.stalemate:
                self.showEndGameMessage("Checkmate" if self.gs.checkmate else "Stalemate",
                                        "Black" if self.gs.whiteToMove else "White")
                running = False
            self.clock.tick(MAX_FPS)
            p.display.flip()

    def handleMouseClick(self, event):
        location = p.mouse.get_pos()  # location of the mouse (x, y)
        if location[0] < WIDTH:  # Click on the board
            col, row = (location[0] // SQ_SIZE), (location[1] // SQ_SIZE)
            if self.sqSelected == (row, col):  # The user clicked the same square twice
                self.sqSelected = None  # Deselect
                self.playerClicks = []  # Clear player clicks
                self.selectedPieceMoves = []  # Clear valid moves for the selected piece
            else:
                self.sqSelected = (row, col)
                self.playerClicks.append(self.sqSelected)  # Append for both 1st and 2nd clicks
                self.selectedPieceMoves = [move for move in self.validMoves if
                                           move.startRow == row and move.startCol == col]
            if len(self.playerClicks) == 2:  # After the 2nd click
                move = Move(self.playerClicks[0], self.playerClicks[1], self.gs.board)
                print(move.getChessNotation())
                for i in range(len(self.validMoves)):
                    if move == self.validMoves[i]:
                        if move.isPawnPromotion:
                            choice = self.showPromotionChoices(self.gs.whiteToMove)
                            self.gs.makeMove(self.validMoves[i], choice)
                        else:
                            self.gs.makeMove(self.validMoves[i])
                        self.moveMade = True
                        self.sqSelected = None  # Reset user clicks
                        self.playerClicks = []
                        self.selectedPieceMoves = []  # Clear valid moves for the selected piece
                        if move.pieceCaptured != "--":
                            self.capturedPieces[move.pieceCaptured[0]].append(move.pieceCaptured)
                            if not isMuted:
                                p.mixer.Sound('sounds/capture.mp3').play()
                        else:
                            if not isMuted:
                                p.mixer.Sound('sounds/move-self.mp3').play()
                if not self.moveMade:
                    self.playerClicks = [self.sqSelected]

    def handleKeyPress(self, event):
        if event.key == p.K_z:
            self.gs.undoMove()
            self.moveMade = True
        elif event.key == p.K_r:
            self.resetGame()
        elif event.key == p.K_ESCAPE:
            self.showESCWindow()

    def showESCWindow(self):
        global isMuted
        if not p.font.get_init():
            p.font.init()
        font = p.font.SysFont("Corbel", 35, bold=True)
        background = p.transform.scale(p.image.load("images/Background.png"), (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))
        
        titleText = font.render("Settings", True, (0, 0, 0))
        titleLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - titleText.get_width() // 2, HEIGHT // 4 - titleText.get_height() // 2)
        self.screen.blit(titleText, titleLocation)
        
        buttonWidth, buttonHeight = 300, 60
        muteButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 - 50, buttonWidth, buttonHeight)
        mainMenuButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 20, buttonWidth, buttonHeight)
        quitButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 90, buttonWidth, buttonHeight)
        backButton = p.Rect(10, 10, 100, 50)
        
        muteIcon = p.transform.scale(p.image.load("images/mute.png"), (30, 30))
        volumeIcon = p.transform.scale(p.image.load("images/volume.png"), (30, 30))
        
        waiting = True
        
        while waiting:
            mouse = p.mouse.get_pos()
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    if muteButton.collidepoint(mouse):
                        isMuted = self.handleMuteToggle()
                    elif mainMenuButton.collidepoint(mouse):
                        p.quit()
                        self.resetGame()
                        self.initializeGame()
                        self.mainLoop()
                        waiting = False
                    elif quitButton.collidepoint(mouse):
                        p.quit()
                        exit()
                    elif backButton.collidepoint(mouse):
                        return
            
            self.screen.blit(background, (0, 0))
            self.screen.blit(titleText, titleLocation)
            
            if muteButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), muteButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), muteButton, border_radius=10)
            
            if mainMenuButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), mainMenuButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), mainMenuButton, border_radius=10)
            
            if quitButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), quitButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), quitButton, border_radius=10)
            
            if backButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), backButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), backButton, border_radius=10)
            
            muteText = font.render("Mute Volume", True, (255, 255, 255))
            mainMenuText = font.render("Main Menu", True, (255, 255, 255))
            quitText = font.render("Quit", True, (255, 255, 255))
            backText = font.render("Back", True, (255, 255, 255))
            self.screen.blit(muteText, muteButton.move(buttonWidth // 2 - muteText.get_width() // 2 - 20, 10))
            self.screen.blit(mainMenuText, mainMenuButton.move(buttonWidth // 2 - mainMenuText.get_width() // 2, 10))
            self.screen.blit(quitText, quitButton.move(buttonWidth // 2 - quitText.get_width() // 2, 10))
            self.screen.blit(backText, backButton.move(backButton.width // 2 - backText.get_width() // 2, 10))
            
            icon = muteIcon if isMuted else volumeIcon
            self.screen.blit(icon, muteButton.move(buttonWidth // 2 + muteText.get_width() // 2, 15))
            
            p.display.flip()

    def handleAIMove(self):
        if not self.validMoves:
            return
        AIMove = computer.findBestMoveAlphaBeta(self.gs, self.validMoves, AI_Depth)
        if AIMove is None:
            AIMove = computer.findRandomMove(self.validMoves)
        self.gs.makeMove(AIMove)
        self.moveMade = True
        if not isMuted:
            if AIMove.pieceCaptured != "--":
                self.capturedPieces[AIMove.pieceCaptured[0]].append(AIMove.pieceCaptured)
                p.mixer.Sound('sounds/capture.mp3').play()
            else:
                p.mixer.Sound('sounds/move-self.mp3').play()

    def resetGame(self):
        self.gs = GameState()
        self.validMoves = self.gs.getValidMoves()
        self.sqSelected = None
        self.playerClicks = []
        self.selectedPieceMoves = []
        self.capturedPieces = {"w": [], "b": []}
        self.moveMade = False

    def drawGameState(self):
        self.drawBoard()
        self.drawPieces()
        self.drawSidebar()

    def drawBoard(self):
        colors = [p.Color("#ecae6a"), p.Color("#794915")]
        selectedColor = p.Color("#68741c")  # Color for the selected square
        moveColor = p.Color("#a7b382")  # Color for valid move squares
        moveColorLight = p.Color("#c9d4a0")  # Lighter color for valid move squares on dark squares
        checkColor = p.Color("red")  # Color for the king in check
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                if self.sqSelected == (r, c):  # Check if this square is selected
                    color = selectedColor
                elif (r, c) in [(move.endRow, move.endCol) for move in self.selectedPieceMoves]:  # Check if this square is a valid move
                    color = moveColorLight if colors[(r + c) % 2] == p.Color("#794915") else moveColor
                else:
                    color = colors[((r + c) % 2)]
                p.draw.rect(self.screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                # Check Color
                if self.gs.inCheck and ((self.gs.whiteToMove and (r, c) == self.gs.whiteKingLocation) or
                                        (not self.gs.whiteToMove and (r, c) == self.gs.blackKingLocation)):
                    color = checkColor
                # Check Sound
                if self.gs.inCheck and not hasattr(self.gs, 'checkSoundPlayed'):
                    if not isMuted:
                        p.mixer.Sound('sounds/move-check.mp3').play()
                    self.gs.checkSoundPlayed = True
                elif not self.gs.inCheck:
                    if hasattr(self.gs, 'checkSoundPlayed'):
                        del self.gs.checkSoundPlayed
                # Checkmate Sound
                if self.gs.checkmate and not hasattr(self.gs, 'checkmateSoundPlayed'):
                    if not isMuted:
                        p.mixer.Sound('sounds/chess_com_checkmate.mp3').play()
                    self.gs.checkmateSoundPlayed = True
                elif not self.gs.checkmate:
                    if hasattr(self.gs, 'checkmateSoundPlayed'):
                        del self.gs.checkmateSoundPlayed
                p.draw.rect(self.screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def drawPieces(self):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = self.gs.board[r][c]
                if piece != "--":
                    self.screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def drawSidebar(self):
        # Draw the sidebar background
        sidebarRect = p.Rect(WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
        p.draw.rect(self.screen, p.Color("#464646"), sidebarRect)

        # Set up font
        font = p.font.SysFont("Helvetica", 24, True, False)

        # Display whose turn it is using color
        turnColor = p.Color("white") if self.gs.whiteToMove else p.Color("black")
        turnRect = p.Rect(WIDTH + 10, 10, 30, 30)
        p.draw.rect(self.screen, turnColor, turnRect)

        # Display captured pieces
        yOffset = 60
        pieceSize = SQ_SIZE // 2  # Smaller size for captured pieces
        for color, pieces in self.capturedPieces.items():
            colorText = "White captured:" if color == "w" else "Black captured:"
            colorObject = font.render(colorText, 0, p.Color("Black"))
            self.screen.blit(colorObject, (WIDTH + 10, yOffset))
            yOffset += 30
            xOffset = WIDTH + 10
            for i, piece in enumerate(pieces):
                pieceImage = p.transform.scale(IMAGES[piece], (pieceSize, pieceSize))
                self.screen.blit(pieceImage, (xOffset, yOffset))
                xOffset += pieceSize + 5  # Move to the right for the next piece
                if (i + 1) % 4 == 0:  # Move to the next row after 4 pieces
                    xOffset = WIDTH + 10
                    yOffset += pieceSize + 5  # Add some space between rows
            yOffset += pieceSize + 10  # Add some space between different color sections

    def showStartWindow(self):
        font = p.font.SysFont("Corbel", 35, bold=True)
        background = p.transform.scale(p.image.load("images/Background.png"), (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))
        
        titleText = font.render("Game Mode", True, (0, 0, 0))
        titleLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - titleText.get_width() // 2, HEIGHT // 4 - titleText.get_height() // 2)
        self.screen.blit(titleText, titleLocation)
        
        buttonWidth, buttonHeight = 300, 60
        vsPlayerButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 - 50, buttonWidth, buttonHeight)
        vsComputerButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 20, buttonWidth, buttonHeight)
        settingsButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 90, buttonWidth, buttonHeight)
        

        waiting = True
        while waiting:
            mouse = p.mouse.get_pos()
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    if vsPlayerButton.collidepoint(mouse):
                        return True, True
                    elif vsComputerButton.collidepoint(mouse):
                        one, two = self.showColorChoiceWindow()
                        if not one and not two:
                            continue
                        return one, two
                    elif settingsButton.collidepoint(mouse):
                        self.showSettingsWindow()
            
            self.screen.blit(background, (0, 0))
            self.screen.blit(titleText, titleLocation)
            
            if vsPlayerButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), vsPlayerButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), vsPlayerButton, border_radius=10)
            
            if vsComputerButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), vsComputerButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), vsComputerButton, border_radius=10)
            
            if settingsButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), settingsButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), settingsButton, border_radius=10)
            
            vsPlayerText = font.render("Player vs Player", True, (255, 255, 255))
            vsComputerText = font.render("Player vs AI", True, (255, 255, 255))
            settingsText = font.render("Settings", True, (255, 255, 255))
            self.screen.blit(vsPlayerText, vsPlayerButton.move(buttonWidth // 2 - vsPlayerText.get_width() // 2, 10))
            self.screen.blit(vsComputerText, vsComputerButton.move(buttonWidth // 2 - vsComputerText.get_width() // 2, 10))
            self.screen.blit(settingsText, settingsButton.move(buttonWidth // 2 - settingsText.get_width() // 2, 10))
            
            p.display.flip()

    def showSettingsWindow(self):
        global isMuted
        font = p.font.SysFont("Corbel", 35, bold=True)
        background = p.transform.scale(p.image.load("images/Background.png"), (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))
        
        titleText = font.render("Settings", True, (0, 0, 0))
        titleLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - titleText.get_width() // 2, HEIGHT // 4 - titleText.get_height() // 2)
        self.screen.blit(titleText, titleLocation)
        
        buttonWidth, buttonHeight = 300, 60
        difficultySlider = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 - 50, buttonWidth, buttonHeight)
        muteButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 20, buttonWidth, buttonHeight)
        backButton = p.Rect(10, 10, 100, 50)
        
        muteIcon = p.transform.scale(p.image.load("images/mute.png"), (30, 30))
        volumeIcon = p.transform.scale(p.image.load("images/volume.png"), (30, 30))
        
        waiting = True
        
        while waiting:
            mouse = p.mouse.get_pos()
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    if difficultySlider.collidepoint(mouse):
                        self.handleDifficultyChange()
                    elif muteButton.collidepoint(mouse):
                        isMuted = self.handleMuteToggle()
                    elif backButton.collidepoint(mouse):
                        return
            
            self.screen.blit(background, (0, 0))
            self.screen.blit(titleText, titleLocation)
            
            if difficultySlider.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), difficultySlider, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), difficultySlider, border_radius=10)
            
            if muteButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), muteButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), muteButton, border_radius=10)
            
            if backButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), backButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), backButton, border_radius=10)
            
            difficultyText = font.render("AI Difficulty", True, (255, 255, 255))
            muteText = font.render("Mute Volume", True, (255, 255, 255))
            backText = font.render("Back", True, (255, 255, 255))
            self.screen.blit(difficultyText, difficultySlider.move(buttonWidth // 2 - difficultyText.get_width() // 2, 10))
            self.screen.blit(muteText, muteButton.move(buttonWidth // 2 - muteText.get_width() // 2 - 20, 10))
            self.screen.blit(backText, backButton.move(backButton.width // 2 - backText.get_width() // 2, 10))
            
            icon = muteIcon if isMuted else volumeIcon
            self.screen.blit(icon, muteButton.move(buttonWidth // 2 + muteText.get_width() // 2, 15))
            
            p.display.flip()

    def handleDifficultyChange(self):
        global AI_Depth
        # Implement a simple difficulty change mechanism
        font = p.font.SysFont("Corbel", 35, bold=True)
        background = p.transform.scale(p.image.load("images/Background.png"), (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))

        titleText = font.render("Select AI Difficulty", True, (0, 0, 0))
        titleLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - titleText.get_width() // 2, HEIGHT // 4 - titleText.get_height() // 2)
        self.screen.blit(titleText, titleLocation)

        buttonWidth, buttonHeight = 200, 50
        difficultyButtons = [p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 - 100 + i * 60, buttonWidth, buttonHeight) for i in range(3)]
        difficultyLevels = ["Level 1", "Level 2", "Level 3"]

        waiting = True
        while waiting:
            mouse = p.mouse.get_pos()
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    for i, button in enumerate(difficultyButtons):
                        if button.collidepoint(mouse):
                            AI_Depth = i + 1
                            waiting = False

            self.screen.blit(background, (0, 0))
            self.screen.blit(titleText, titleLocation)

            for i, button in enumerate(difficultyButtons):
                if button.collidepoint(mouse) or AI_Depth == i + 1:
                    p.draw.rect(self.screen, (0, 255, 0) if AI_Depth == i + 1 else (170, 170, 170), button, border_radius=10)
                else:
                    p.draw.rect(self.screen, (100, 100, 100), button, border_radius=10)
                difficultyText = font.render(difficultyLevels[i], True, (255, 255, 255))
                self.screen.blit(difficultyText, button.move(buttonWidth // 2 - difficultyText.get_width() // 2, 10))

            p.display.flip()

    def handleMuteToggle(self):
        global isMuted
        # Implement a simple mute toggle mechanism
        if p.mixer.get_init():
            if p.mixer.music.get_volume() > 0:
                p.mixer.music.set_volume(0)
                isMuted = True
            else:
                p.mixer.music.set_volume(1)
                isMuted = False
        return isMuted

    def showColorChoiceWindow(self):
        font = p.font.SysFont("Corbel", 35, bold=True)
        background = p.transform.scale(p.image.load("images/Background.png"), (WIDTH, HEIGHT))
        self.screen.blit(background, (0, 0))

        titleText = font.render("Choose Color", True, (0, 0, 0))
        titleLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - titleText.get_width() // 2, HEIGHT // 4 - titleText.get_height() // 2)
        self.screen.blit(titleText, titleLocation)

        whiteButton = p.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        blackButton = p.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
        backButton = p.Rect(10, 10, 100, 50)

        waiting = True
        while waiting:
            mouse = p.mouse.get_pos()
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    if whiteButton.collidepoint(mouse):
                        return True, False
                    elif blackButton.collidepoint(mouse):
                        return False, True
                    elif backButton.collidepoint(mouse):
                        return False, False
            
            self.screen.blit(background, (0, 0))
            self.screen.blit(titleText, titleLocation)
            
            if whiteButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), whiteButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (255, 255, 255), whiteButton, border_radius=10)
            
            if blackButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), blackButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (0, 0, 0), blackButton, border_radius=10)
            
            if backButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), backButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), backButton, border_radius=10)
            
            whiteText = font.render("White", True, (0, 0, 0))
            blackText = font.render("Black", True, (255, 255, 255))
            backText = font.render("Back", True, (255, 255, 255))
            self.screen.blit(whiteText, whiteButton.move(60, 10))
            self.screen.blit(blackText, blackButton.move(60, 10))
            self.screen.blit(backText, backButton.move(backButton.width // 2 - backText.get_width() // 2, 10))
            
            p.display.flip()

    def showPromotionChoices(self, isWhite):
        buttonWidth, buttonHeight = 200, 50
        queenButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 - 60, buttonWidth, buttonHeight)
        rookButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2, buttonWidth, buttonHeight)
        knightButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 60, buttonWidth, buttonHeight)
        bishopButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 120, buttonWidth, buttonHeight)

        buttons = [(queenButton, "Q"), (rookButton, "R"), (knightButton, "N"), (bishopButton, "B")]
        pieceIcons = {
            "Q": IMAGES["wQ"] if isWhite else IMAGES["bQ"],
            "R": IMAGES["wR"] if isWhite else IMAGES["bR"],
            "N": IMAGES["wN"] if isWhite else IMAGES["bN"],
            "B": IMAGES["wB"] if isWhite else IMAGES["bB"]
        }

        waiting = True
        while waiting:
            mouse = p.mouse.get_pos()
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    for button, piece in buttons:
                        if button.collidepoint(mouse):
                            return piece
            
            for button, piece in buttons:
                if button.collidepoint(mouse):
                    p.draw.rect(self.screen, (170, 170, 170), button, border_radius=10)
                else:
                    p.draw.rect(self.screen, (100, 100, 100), button, border_radius=10)
                pieceIcon = p.transform.scale(pieceIcons[piece], (buttonHeight, buttonHeight))
                self.screen.blit(pieceIcon, button.move(buttonWidth // 2 - buttonHeight // 2, 0))
            
            p.display.flip()

    def showEndGameMessage(self, message, winner):
        font = p.font.SysFont("Corbel", 35, bold=True)

        if winner:
            if message == "Checkmate":
                message = f"{winner} wins by checkmate!"
            else:
                message = "It's a stalemate!"

        titleText = font.render(message, True, (0, 0, 0))
        titleLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - titleText.get_width() // 2, HEIGHT // 4 - titleText.get_height() // 2)
        
        # Create a semi-transparent overlay
        overlay = p.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)  # Set transparency level
        overlay.fill((255, 255, 255))  # Fill with white color
        self.screen.blit(overlay, (0, 0))
        
        self.screen.blit(titleText, titleLocation)

        buttonWidth, buttonHeight = 200, 50
        playAgainButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 10, buttonWidth, buttonHeight)
        mainMenuButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 70, buttonWidth, buttonHeight)
        quitButton = p.Rect(WIDTH // 2 - buttonWidth // 2, HEIGHT // 2 + 130, buttonWidth, buttonHeight)

        waiting = True
        while waiting:
            mouse = p.mouse.get_pos()
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    if playAgainButton.collidepoint(mouse):
                        self.resetGame()
                        self.mainLoop()
                        waiting = False
                    elif mainMenuButton.collidepoint(mouse):
                        self.initializeGame()
                        self.mainLoop()
                        waiting = False
                    elif quitButton.collidepoint(mouse):
                        p.quit()
                        exit()
            
            self.screen.blit(titleText, titleLocation)
            
            if playAgainButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), playAgainButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), playAgainButton, border_radius=10)
            
            if mainMenuButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), mainMenuButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), mainMenuButton, border_radius=10)
            
            if quitButton.collidepoint(mouse):
                p.draw.rect(self.screen, (170, 170, 170), quitButton, border_radius=10)
            else:
                p.draw.rect(self.screen, (100, 100, 100), quitButton, border_radius=10)
            
            playAgainText = font.render("Play Again", True, (255, 255, 255))
            mainMenuText = font.render("Main Menu", True, (255, 255, 255))
            quitText = font.render("Quit", True, (255, 255, 255))
            self.screen.blit(playAgainText, playAgainButton.move(buttonWidth // 2 - playAgainText.get_width() // 2, 10))
            self.screen.blit(mainMenuText, mainMenuButton.move(buttonWidth // 2 - mainMenuText.get_width() // 2, 10))
            self.screen.blit(quitText, quitButton.move(buttonWidth // 2 - quitText.get_width() // 2, 10))
            
            p.display.flip()

if __name__ == "__main__":
    game = ChessGame()
    game.initializeGame()
    game.mainLoop()
