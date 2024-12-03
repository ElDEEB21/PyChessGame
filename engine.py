class GameState():
    
    def __init__(self):
        # Board is an 8x8 2D List, each element of the list has 2 characters.
        # The first character represents the color of the piece (b/w)
        # The second character represents the type of the piece (R, N, B, Q, K, p)
        # "--" represents an empty space with no piece.
        # Rooks -> R, Knights -> N, Bishops -> B, Queen -> Q, King -> K, Pawns -> p
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            
    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        moves = [Move((6, 4), (4, 4), self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if (self.whiteToMove and turn == "w") or (not self.whiteToMove and turn == "b"):
                    if piece == "p":
                        self.getPawnMoves(r, c, moves)
                    elif piece == "R":
                        self.getRookMoves(r, c, moves)
                    elif piece == "N":
                        self.getKnightMoves(r, c, moves)
                    elif piece == "B":
                        self.getBishopMoves(r, c, moves)
                    elif piece == "Q":
                        self.getQueenMoves(r, c, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, moves)
        return moves
    
    def getPawnMoves(self, r, c, moves):
        pass
    
    def getRookMoves(self, r, c, moves):
        pass
    
    def getKnightMoves(self, r, c, moves):
        pass
    
    def getBishopMoves(self, r, c, moves):
        pass
    
    def getQueenMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass
    
    
        
class Move():
    # Maps keys to values
    # key : value
    # (row, col) : (row, col)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    