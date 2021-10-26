# main driver file, used for handling user input, and displaying current game-state object.

import pygame as p
import ChessEngine
import ChessAI as AI

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation if need be
IMAGES = {}
'''
initialise a global dictionary of images. This will be called exactly once in the main.
'''
def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
''' 
the main driver for our code. This will handle user input and updating graphics.
'''
def event(gs, validMoves, moveMade, running, sqSelected, playerClicks, screen, clock, humanWhite, humanBlack):
    while running:
        humanTurn = (gs.whiteToMove and humanWhite) or (not gs.whiteToMove and humanBlack)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN and humanTurn:
                location = p.mouse.get_pos()  # (x,y) location of mouse.
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear player-clicks

                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both first and second clicks.
                if len(playerClicks) == 2:  # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation(), move.pieceMoved, move.pieceCaptured)
                    
                    for indx in range(len(validMoves)):
                        if move == validMoves[indx]:
                            gs.makeMove(validMoves[indx])
                            moveMade = True
                            #print("move made")
                            sqSelected = ()  # reset user clicks
                            playerClicks = []
            
                if not moveMade:
                    playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when z is pressed.
                    gs.undoMove()
                    moveMade = True
        
        if not humanTurn:
            AIMove = AI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            humanTurn = not humanTurn

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made
    loadImages()   # only once before while loop
    running = True
    sqSelected = ()  # no square is selected. keep track of last click of user.
    playerClicks = []  # keep track of player-clicks.
    humanWhite = True
    humanBlack = False
   # while running:
    #    for e in p.event.get():
    event(gs, validMoves, moveMade, running, sqSelected, playerClicks, screen, clock, humanWhite, humanBlack)
            #running = event_running[0]
            #moveMade = event_running[1]
            #Trying for checkmate. Not fixed yet. Should only quit if No other move possible
            #if not gs.getValidMoves:
            #   running = False



def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("cornsilk"), p.Color("tan")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

