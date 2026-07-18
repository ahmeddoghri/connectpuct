from connectpuct import choose_move, empty_board

board = empty_board().play(3).play(2).play(3).play(2).play(4)
move = choose_move(board, simulations=40, seed=4)
print(f"ai_move={move} legal={board.legal_moves()}")
