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
        