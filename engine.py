from moves import MoveGenerator, Move

class GameState(MoveGenerator):
    def __init__(self):
        super().__init__()
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
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation , self.blackKingLocation = (7, 4), (0, 4)
        self.inCheck = False
        self.checkmate, self.stalemate = False, False
        self.pins, self.checks = [], []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        """Gets all moves considering checks"""
        valid_moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()

        # Updates king locations
        if self.whiteToMove:
            king_row, king_column = self.whiteKingLocation[0], self.whiteKingLocation[1]
        else:
            king_row, king_column = self.blackKingLocation[0], self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:  # Only 1 check: block check or move king
                valid_moves = self.getAllPossibleMoves()
                check = self.checks[0]
                check_row, check_column = check[0], check[1]
                piece_checking = self.board[check_row][check_column]  # Enemy piece causing check
                valid_squares = []
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_column)]
                else:
                    for i in range(1, len(self.board)):
                        valid_square = (king_row + check[2] * i, king_column + check[3] * i)  # 2 & 3 = check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_column:
                            break
                for i in range(len(valid_moves) - 1, -1, -1):  # Gets rid of move not blocking, checking, or moving king
                    if valid_moves[i].pieceMoved[1] != 'K':
                        if not (valid_moves[i].endRow, valid_moves[i].endCol) in valid_squares:
                            valid_moves.remove(valid_moves[i])
            else:  # Double check, king must move
                self.getKingMoves(king_row, king_column, valid_moves, self.board, self.whiteToMove)
        else:  # Not in check
            valid_moves = self.getAllPossibleMoves()

        if len(valid_moves) == 0:  # Either checkmate or stalemate
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return valid_moves

    def getAllPossibleMoves(self):
        """Gets all moves without considering checks"""
        moves = []
        for row in range(len(self.board)):  # Number of rows
            for column in range(len(self.board[row])):  # Number of columns in each row
                turn = self.board[row][column][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][column][1]
                    self.moveFunctions[piece](row, column, moves, self.board, self.whiteToMove)  # Calls move function based on piece type
        return moves
    
    def checkForPinsAndChecks(self):
        """Returns if the player is in check, a list of pins, and a list of checks"""
        pins = []
        checks = []
        inCheck = False

        if self.whiteToMove:
            opponent = 'b'
            ally = 'w'
            startRow, startCol = self.whiteKingLocation
        else:
            opponent = 'w'
            ally = 'b'
            startRow, startCol = self.blackKingLocation

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # Resets possible pins
            for i in range(1, len(self.board)):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ally and endPiece[1] != 'K':
                        if possiblePin == ():  # 1st ally piece can be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # 2nd ally piece, so no pin or check possible
                            break
                    elif endPiece[0] == opponent:
                        pieceType = endPiece[1]
                        if (0 <= j <= 3 and pieceType == 'R') or (4 <= j <= 7 and pieceType == 'B') or \
                                (i == 1 and pieceType == 'P' and ((opponent == 'w' and 6 <= j <= 7)
                                                                   or (opponent == 'b' and 4 <= j <= 5))) or \
                                (pieceType == 'Q') or (i == 1 and pieceType == 'K'):
                            if possiblePin == ():  # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # Piece blocking, so pin
                                pins.append(possiblePin)
                                break
                        else:  # Enemy piece but not applying check
                            break
                else:  # Off board
                    break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knightMoves:
            endRow = startRow + move[0]
            endCol = startCol + move[1]
            if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == opponent and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, move[0], move[1]))

        return inCheck, pins, checks
    