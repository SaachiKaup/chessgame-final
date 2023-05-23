import random
import ChessEngine
import copy
import sys
pieceScores = {"K": 0, "Q": 900, "R": 500, "N": 325, "B": 300, "p": 100, "-": 0}
CHECKMATE = 1000000
MAX = 1010350 #all pawns get promoted to queens
#ZERO SUM GAME
#White is trying to maximize the score to MAX, black is trying to minimize it to -MAX
#Evaluating based on pieces present in the board.
def findRandomMove(validMoves):
    return random.choice(validMoves)

def getComparer(maxPlayer: bool) -> chr:
    if maxPlayer:
        return '>'
    return '<'

def getComparerString(val, val2Optimize, maxPlayer: bool):
    sign = getComparer(maxPlayer)
    return str(val) + sign + str(val2Optimize)

def getComparerFunction(val, val2Optimize, maxPlayer: bool):
    return eval(getComparerString(val, val2Optimize, maxPlayer))

def finalCondition(depth: int, gs) -> bool:
    return depth < 2 or gs.checkMate

def getSign(maxPlayer = True) -> float:
    if maxPlayer:
        return -1
    return 1
def minimax(gs, bestMove, finalScore, depth = 3, maxPlayer = True, bound = None):
    if finalCondition(depth, gs):
        return (bestMove, getBoardScore(gs.board))

    allMoves = gs.getValidMoves()

    print(f'pieces: {[move.pieceMoved for move in allMoves]}')
    for move in allMoves:
        gsCopy = copy.deepcopy(gs)
        gsCopy.makeMove(move)
        currentScore = getBoardScore(gsCopy.board)
        print(gsCopy.board)
        if bound and getComparerFunction(bound, currentScore, maxPlayer):
            break
        (newMove, newBoardScore) = minimax(gsCopy, move, finalScore, depth - 1, (not maxPlayer), getBoardScore(gsCopy.board))
        print(f'newMove: {newMove.pieceMoved}')
        print("function value", getComparerFunction(finalScore, newBoardScore, maxPlayer))
        if getComparerFunction(finalScore, newBoardScore, maxPlayer):
            finalScore = newBoardScore
            bestMove = newMove

    return (bestMove, finalScore)
def findBestMove(gs, validMoves: [], depth = 3):
    bestMove = validMoves[-1]
    finalScore = getSign() * sys.maxsize
    bestMove, _ = minimax(gs, bestMove, finalScore)
    return bestMove
def _findBestMove(gs, validMoves):
    boardScores = [getBoardScore(gs.board) for _ in validMoves]
    print(f'bf: {gs.board}')
    gsCopy = copy.deepcopy(gs)
    print(f'copy: {gsCopy}')
    #print(getBoardScore(gs.board))
    maxValueMoveIndx = boardScores.index(max(boardScores))
    maxValueMove = validMoves[maxValueMoveIndx]
    startTup = (maxValueMove.startRow, maxValueMove.startCol)
    endTup = (maxValueMove.endRow, maxValueMove.endCol)
    print(f'tups: {startTup}, {endTup}')
    moveMade = ChessEngine.Move(startTup, endTup, gs.board)
    gsCopy.makeMove(moveMade)
    print(f'af: copy: {gsCopy.board}, orig: {gs.board} eq: {gsCopy.board == gs.board}')
    print(f'af: copy: {getBoardScore(gsCopy.board)}, orig: {getBoardScore(gs.board)} move: {moveMade}')
    return validMoves[maxValueMoveIndx]

def getBoardScore(board):
    boardScore = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                #print(square[1])
                boardScore += pieceScores[square[1]]
            else:
                #print(square[1])
                boardScore -= pieceScores[square[1]]
    return boardScore
