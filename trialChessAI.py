import chess, chess.engine, asyncio, time
def get_time():
    return time.perf_counter()

def not_check_or_stale(board):
    return not board.is_checkmate()

def get_info(engine, board, limit):
    return engine.analyse(board, limit)
async def main():
    start = get_time()
    #transport, engine, not simple
    
    transport, engine = await chess.engine.popen_uci("/usr/games/stockfish")
    board = chess.Board()
    print(f'Start Board:\n{board}')
    limit = chess.engine.Limit(time = 0.1, depth = 3)
    while not_check_or_stale(board):
        move = chess.Move.from_uci(input("Enter move:"))
        print(f'{move}')
        if move:
            board.push(move)
            print(f'\n{board}')
        
        result = await engine.play(board, limit)
        if result.move:
            print(f'{result.move}')
            board.push(result.move)
            print(f'\n{board}')
            info = await get_info(engine, board, limit)
            print(f'{info["score"]}')
 
    await engine.quit()
    end = get_time() - start
    print(f'time taken: {end:0.2f}')

asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
asyncio.run(main())
#main() to check time without waiting asynchronously: much larger

