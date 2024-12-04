class MoveGenerator:
    
    def getPawnMoves(self, r, c, moves, board, whiteToMove):
        if whiteToMove:
            if board[r - 1][c] == "--":  # 1 square move
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
            if board[r + 1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r + 1, c), board))
                if r == 1 and board[r+2][c] == "--":  # 2 square move
                    moves.append(Move((r, c), (r + 2, c), board))
            if c - 1 >= 0:
                if board[r + 1][c - 1][0] == "w":  # Capture to the left
                    moves.append(Move((r, c), (r + 1, c - 1), board))
            if c + 1 < len(board):
                if board[r + 1][c + 1][0] == "w":  # Capture to the right
                    moves.append(Move((r, c), (r + 1, c + 1), board))
        # TODO: Add pawn promotion      

    def getRookMoves(self, r, c, moves, board, whiteToMove):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # Up, Left, Down, Right
        enemyColor = "b" if whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(board) and 0 <= endCol < len(board[0]):
                    endPiece = board[endRow][endCol]
                    if endPiece == "--":  # Empty space valid
                        moves.append(Move((r, c), (endRow, endCol), board))
                    elif endPiece[0] == enemyColor:  # Capture enemy piece
                        moves.append(Move((r, c), (endRow, endCol), board))
                        break
                    else:  # Friendly piece invalid
                        break
                else:  # Off board
                    break

    def getKnightMoves(self, r, c, moves, board, whiteToMove):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)) # L-shaped moves
        allyColor = "w" if whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < len(board) and 0 <= endCol < len(board[0]):
                endPiece = board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), board))
        
    def getBishopMoves(self, r, c, moves, board, whiteToMove):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # Up-Left, Up-Right, Down-Left, Down-Right
        enemyColor = "b" if whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(board) and 0 <= endCol < len(board[0]):
                    endPiece = board[endRow][endCol]
                    if endPiece == "--":  # Empty space valid
                        moves.append(Move((r, c), (endRow, endCol), board))
                    elif endPiece[0] == enemyColor:  # Capture enemy piece
                        moves.append(Move((r, c), (endRow, endCol), board))
                        break
                    else:  # Friendly piece invalid
                        break
                else:  # Off board
                    break
        
    def getQueenMoves(self, r, c, moves, board, whiteToMove):
        self.getRookMoves(r, c, moves, board, whiteToMove)
        self.getBishopMoves(r, c, moves, board, whiteToMove)

    def getKingMoves(self, r, c, moves, board, whiteToMove):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))  # All possible king moves
        allyColor = "w" if whiteToMove else "b"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < len(board) and 0 <= endCol < len(board[0]):
                endPiece = board[endRow][endCol]
                if endPiece == "--" or endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), board))
    
    
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