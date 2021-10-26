import random
pieceScores = {"K": 0, "Q": 900, "R": 500, "N": 325, "B": 300, "p": 100}
CHECKMATE = 100000
MAX = 110350 #all pawns get promoted to queens
#ZERO SUM GAME
#White is trying to maximize the score to MAX, black is trying to minimize it to -MAX
#Evaluating based on pieces present in the board.
def findRandomMove(validMoves):
    return random.choice(validMoves)

def findBestMove(gs, validMoves):
    boardScores = [getBoardScore(gs.board) for playerMove in validMoves]
    print(f'{boardScores}')
    pass

def getBoardScore(board):
    boardScore = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                boardScore += pieceScores[square[1]]
            else:
                boardScore -= pieceScores[square[1]]
    return boardScore
