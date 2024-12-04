class MoveGenerator:
    def getPawnMoves(self, r, c, moves, board, whiteToMove):
        if whiteToMove:
            if board[r-1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r - 1, c), board))
                if r == 6 and board[r-2][c] == "--":  # 2 square move
                    moves.append(Move((r, c), (r - 2, c), board))
            if c - 1 >= 0:
                if board[r - 1][c - 1][0] == "b":  # Capture to the left
                    moves.append(Move((r, c), (r - 1, c - 1), board))
            if c + 1 < len(board):
                if board[r - 1][c + 1][0] == "b":  # Capture to the right
                    moves.append(Move((r, c), (r - 1, c + 1), board))
        else:
            # Implement black pawn moves here
            pass

    def getRookMoves(self, r, c, moves, board, whiteToMove):
        pass

    def getKnightMoves(self, r, c, moves, board, whiteToMove):
        pass

    def getBishopMoves(self, r, c, moves, board, whiteToMove):
        pass

    def getQueenMoves(self, r, c, moves, board, whiteToMove):
        pass

    def getKingMoves(self, r, c, moves, board, whiteToMove):
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