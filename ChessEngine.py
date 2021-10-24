# storing all information about current state of Chess game.
# Also responsible for determining valid moves at current stats.
import itertools as it
class GameState():
    def __init__(self):
        self.board =[
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'R': self.getRookMoves, 'p': self.getPawnMoves,\
                'K': self.getKingMoves, 'B': self.getBishopMoves,\
                'N': self.getKnightMoves, 'Q': self.getQueenMoves}
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # logging the move so we can undo it later.
        self.whiteToMove = not self.whiteToMove  # swap players
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
    def undoMove(self):
        if len(self.moveLog) != 0:  # making sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back.
    
    def getReverseBoard(self):
        pass

    def getEndLessOrStart(self, start, end):
        if start < end:
            return (start, end)
        return (end, start)
     
    def getValidMoves(self):
        moves = self.getAllPossibleMoves() #just because validity of moves must be checked
        #for move in self.moveLog:
            #print(move.pieceMoved)
        for i in range(len(moves) - 1, -1, -1): #traverses moves backwards
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.squareUnderAttack():
                print(move.pieceMoved, move.pieceCaptured)
                del moves[i]
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        if len(moves) == 0:
            if self.squareUnderAttack():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate, self.staleMate = False, False
        
        return moves
     
    def squareUnderAttack(self):
        self.whiteToMove = not self.whiteToMove #perspective switch
        opp_moves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in opp_moves:
            if not self.whiteToMove and move.pieceCaptured == 'wK':
                return True
            elif self.whiteToMove and self.board[move.endRow][move.endCol] == 'bK':
                return True
        return False


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

    def getEnemyOrAlly(self, whiteToMove, isEnemy = True):
        if isEnemy:
            return 'b' if whiteToMove else 'w'
        return 'w' if whiteToMove else 'b'

    def pawnMovesWB(self, r, c, moves, toWhite = False):
        sign = -1
        row = 1
        enemy = self.getEnemyOrAlly(toWhite, isEnemy = True)
        if toWhite:
            sign = 1
            row = 6
        if r == row and self.board[r - (sign * 2)][c] == '--':
            moves.append(Move((r,c), (r - (sign * 2), c), self.board))
        if r - (sign * 1) in range(0, 8):
            if self.board[r - (sign * 1)][c] == "--":
                moves.append(Move((r,c), (r - (sign * 1), c), self.board))
            if c - 1 in range(0, 8) and self.board[r -(sign * 1)][c - 1][0] == enemy:
                moves.append(Move((r,c), (r - (sign * 1), c - 1), self.board))
            if c + 1 in range(0, 8) and self.board[r - (sign * 1)][c + 1][0] == enemy:
                moves.append(Move((r,c), (r - (sign * 1), c + 1), self.board))
        
    def getPawnMoves(self, r, c, moves): #r and c are rows and columns entered by user
        if self.whiteToMove:
            self.pawnMovesWB(r, c, moves, True)
        else:
            self.pawnMovesWB(r, c, moves, False)
    
    def checkEmptySquare(self, mid_row_indx, mid_col_indx):
        return self.board[mid_row_indx][mid_col_indx] == '--'

    def checkRookPath(self, r, c, endRow, endCol, direction):
        if direction[0] != 0:
            rowOrdered = self.getEndLessOrStart(r, endRow)
            if all([(self.board[mid_path_row_indx][endCol] == '--') for mid_path_row_indx in range(rowOrdered[0] + 1, rowOrdered[1])]):
                return True
        elif direction[1] != 0:
            colOrdered = self.getEndLessOrStart(c, endCol) 
            if all([(self.board[endRow][mid_path_col_indx] == '--') for mid_path_col_indx in range(colOrdered[0] + 1, colOrdered[1])]):
                return True
        return False

    def getRookMoves(self, r, c, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        enemy = self.getEnemyOrAlly(self.whiteToMove, True)
        for direction in directions:    
            for indx in range(1, 8):
                endRow = r + direction[0] * indx
                endCol = c + direction[1] * indx
                if endRow in range(0, 8) and endCol in range(0,8)\
                        and self.checkRookPath(r, c, endRow, endCol, direction):
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
        ally = self.getEnemyOrAlly(self.whiteToMove, False)
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

    def checkBishopPath(self, r, c, endRow, endCol):
        #Cases
        #r < endRow 
            #c < EndCol
            #c > end COl
        if r < endRow:
            if c < endCol:
                col = c + 1 
                for row in range(r + 1, endRow):
                    if self.board[row][col] == '--':
                        print("col, ", col, "row", row)
                        col += 1
                    else:
                        return False
            else:
                col = c - 1
                for row in range(r + 1, endRow):
                    if self.board[row][col] == '--':
                        col -= 1
                    else:
                        return False
        else:# r> endRow
            if c < endCol:
                col = c + 1
                for row in range(r - 1, endRow, -1):
                    if self.board[row][col] == '--':
                        col += 1
                    else:
                        return False
            else:#c  >EndCOl
                col = c - 1
                for row in range(r - 1, endRow, -1):
                    if self.board[row][col] == '--':
                        col -= 1
                    else:
                        return False
        return True

    def getBishopMoves(self, r, c, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        enemy = self.getEnemyOrAlly(self.whiteToMove, isEnemy = True)
        
        for direction in directions:
            for indx in range(1, 8):
                
                endRow = r + direction[0] * indx
                endCol = c + direction[1] * indx
                
                if endRow in range(0, 8) and endCol in range(0,8)\
                        and self.checkBishopPath(r, c, endRow, endCol):
                    
                    endPiece = self.board[endRow][endCol]
                    
                    if endPiece[0] == enemy or endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        king_move = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (1, 1), (-1, 1), (-1,-1)]
        ally = self.getEnemyOrAlly(self.whiteToMove, False)
        for indx in range(8):
            endRow = r + king_move[indx][0]
            endCol = c + king_move[indx][1]
            if endRow in range(8) and endCol in range(8):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                else:
                    break
            else:
                break

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
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)

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
