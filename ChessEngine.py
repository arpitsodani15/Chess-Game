"""
This class is responsible for storing all the information about the current state of a chess game. It will also be responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState:

    def __init__(self):
        # board is an 8x8 2D list, each element of the list has 2 characters,
        # The first represents the color black or white,
        # The second represents the type of piece, 'K', 'Q', 'R', 'B', 'N', or 'p'
        # "--" represents the empty spaces,
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []

    """"
    Takes a move as parameter and executes it (this will not work for castling, pawn promotion and en-passant)
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players

    """
    Undo the last move
    """
    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undoMove
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # swap turns back

    """
    All moves considering checks
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    """
    All moves without considering checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # no. of rows
            for c in range(len(self.board[r])):  # no. of cols
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        moves.extend(self.getPawnMoves(r, c))
                    elif piece == 'R':
                        moves.extend(self.getRookMoves(r, c))
                    elif piece == 'N':
                        moves.extend(self.getKnightMoves(r, c))
                    elif piece == 'B':
                        moves.extend(self.getBishopMoves(r, c))
                    elif piece == 'K':
                        moves.extend(self.getKingMoves(r, c))
                    elif piece == 'Q':
                        moves.extend(self.getQueenMoves(r, c))
        return moves

    """
    Get all pawn moves
    """
    def getPawnMoves(self, r, c):
        moves = []
        if self.board[r][c][0] == 'b':  # if pawn is black
            # diagonal move when there is a white diagonally
            if r + 1 < len(self.board) and c + 1 < len(self.board[r]) and self.board[r + 1][c + 1][0] == 'w':
                moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if r + 1 < len(self.board) and c - 1 >= 0 and self.board[r + 1][c - 1][0] == 'w':
                moves.append(Move((r, c), (r + 1, c - 1), self.board))
            # normal move
            if r + 1 < len(self.board) and self.board[r + 1][c][0] == '-':
                moves.append(Move((r, c), (r + 1, c), self.board))
            # at start double steps
            if r == 1 and self.board[r + 2][c][0] == '-':
                moves.append(Move((r, c), (r + 2, c), self.board))

        elif self.board[r][c][0] == 'w':  # if pawn is white
            # diagonal move when there is a black diagonally
            if r - 1 >= 0 and c + 1 < len(self.board[r]) and self.board[r - 1][c + 1][0] == 'b':
                moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if r - 1 >= 0 and c - 1 >= 0 and self.board[r - 1][c - 1][0] == 'b':
                moves.append(Move((r, c), (r - 1, c - 1), self.board))
            # normal move
            if r - 1 >= 0 and self.board[r - 1][c][0] == '-':
                moves.append(Move((r, c), (r - 1, c), self.board))
            # at start double steps
            if r == 6 and self.board[r - 2][c][0] == '-':
                moves.append(Move((r, c), (r - 2, c), self.board))

        return moves

    """
    Get all rook moves
    """
    def getRookMoves(self, r, c):
        moves = []
        canKill = 'w' if self.board[r][c][0] == 'b' else 'b'
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for (x, y) in direction:
            newR, newC = r + x, c + y
            while len(self.board) > newR >= 0 and len(self.board[r]) > newC >= 0:
                if self.board[newR][newC][0] == '-' or self.board[newR][newC][0] == canKill:
                    moves.append(Move((r, c), (newR, newC), self.board))
                else:
                    break;
                newR, newC = newR + x, newC + y

        return moves

    """
    Get all Knight moves
    """
    def getKnightMoves(self, r, c):
        moves = []
        canKill = 'w' if self.board[r][c][0] == 'b' else 'b'
        direction = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for (x, y) in direction:
            if (len(self.board) > r + x >= 0 and len(self.board[r]) > c + y >= 0) and (self.board[r+x][c+y][0] == '-' or self.board[r+x][c+y][0] == canKill):
                moves.append(Move((r, c), (r+x, c+y), self.board));

        return moves

    """
    Get all Bishop moves
    """
    def getBishopMoves(self, r, c):
        moves = []
        canKill = 'w' if self.board[r][c][0] == 'b' else 'b'
        direction = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for (x, y) in direction:
            newR, newC = r+x, c+y
            while len(self.board) > newR >= 0 and len(self.board[r]) > newC >= 0:
                if self.board[newR][newC][0] == '-' or self.board[newR][newC][0] == canKill:
                    moves.append(Move((r, c), (newR, newC), self.board))
                else:
                    break;
                newR, newC = newR + x, newC + y

        return moves

    """
    Get all King moves
    """
    def getKingMoves(self, r, c):
        moves = []
        canKill = 'w' if self.board[r][c][0] == 'b' else 'b'
        direction = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for (x, y) in direction:
            newR, newC = r + x, c + y
            if len(self.board) > newR >= 0 and len(self.board[r]) > newC >= 0:
                if self.board[newR][newC][0] == '-' or self.board[newR][newC][0] == canKill:
                    moves.append(Move((r, c), (newR, newC), self.board))

        return moves

    """
    Get all Queen Moves
    """
    def getQueenMoves(self, r, c):
        moves = []
        moves.extend(self.getBishopMoves(r, c))
        moves.extend(self.getRookMoves(r, c))
        return moves



"""
Move class is the used to form a move structure
"""


class Move:
    # maps keys to values in the (key : value)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # Unique move ID to each move
        self.moveID = (self.startRow * 1000) + (self.startCol * 100) + (self.endRow * 10) + (self.endCol)

    """
    Overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
