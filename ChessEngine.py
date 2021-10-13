# storing all information about current state of Chess game.
# Also responsible for determining valid moves at current stats.
class GameState():
    def __init__(self):
        self.board =[
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "bp", "bR", "--", "wR", "bR", "--", "--"],
            ["--", "--", "--", "wR", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wR", "bR", "bp", "--", "bp", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'R': self.getRookMoves, 'p': self.getPawnMoves,\
                'K': self.getKingMoves, 'B': self.getBishopMoves,\
                'N': self.getKnightMoves, 'Q': self.getQueenMoves}

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # logging the move so we can undo it later.
        self.whiteToMove = not self.whiteToMove  # swap players


    def undoMove(self):
        if len(self.moveLog) != 0:  # making sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back.

    '''
    all moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    all moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove)\
                        or (turn =='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    '''
    Get all the pawn moves for the pawn located at  row, col and  add these moves to the  list
    '''
    def pawnMovesWB(self, r, c, moves, toWhite = False):
        sign = -1
        row = 1
        enemy_pawn = 'w'
        if toWhite:
            sign = 1
            row = 6
            enemy_pawn = 'b'
        if r == row and self.board[r - (sign * 2)][c] == '--':
            moves.append(Move((r,c), (r - (sign * 2), c), self.board))
        if self.board[r - (sign * 1)][c] == "--":
            moves.append(Move((r,c), (r - (sign * 1), c), self.board))
        if c - 1 >= 0 and self.board[r -(sign * 1)][c - 1][0] == enemy_pawn:
            moves.append(Move((r,c), (r - (sign * 1), c - 1), self.board))
        if c + 1 <= 7 and self.board[r - (sign * 1)][c + 1][0] == enemy_pawn:
            moves.append(Move((r,c), (r - (sign * 1), c + 1), self.board))

    def getPawnMoves(self, r, c, moves): #r and c are rows and columns entered by user
        if self.whiteToMove:
            self.pawnMovesWB(r, c, moves, True)
        else:
            self.pawnMovesWB(r, c, moves, False)
    
   # def check_row_path(self, board, r, c, next_pos, sign) -> bool:
    #    if sign == 1:
     #       for mid_pos in range(r + 1, next_pos):
      #          board_c_notation = board[mid_pos][c][0]
       #         if board_c_notation == 'w' or board_c_notation == 'b':
        #            print("False: ", board[mid_pos][c])
         #           return False
       # print("TRUE")
        #return True

    def getRookMoves(self, r, c, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        enemy = 'w'
        if self.whiteToMove:
            enemy = 'b'
        for direction in directions:    
            for indx in range(1, 8):
                endRow = r + direction[0] * indx
                endCol = c + direction[1] * indx
                if endRow in range(0, 8) and endCol in range(0,8):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--' or endPiece[0] == enemy:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        break
                else:
                    break
                    
    def getKnightMoves(self, r, c, moves):
        directions = [(2, 1), (2, -1), (1, 2), (1, -2),\
                (-2, 1), (-2, -1), (-1, 2), (-1, -1)]
        ally = 'w' if self.whiteToMove else 'b'
        for direction in directions:
            for indx in range(1, 8):
                endRow = r + direction[0] * indx
                endCol = c + direction[1] * indx
                if endRow in range(0, 8) and endCol in range(0,8):
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != ally:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        pass

    def getQueenMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass


class Move():

    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self,startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
