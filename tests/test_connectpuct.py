from connectpuct import choose_move, empty_board
from connectpuct.engine import Board


def test_vertical_win_detection() -> None:
    board = empty_board()
    for _ in range(3):
        board = board.play(0).play(1)
    board = board.play(0)
    assert board.winner() == 1


def test_illegal_full_column_rejected() -> None:
    board = empty_board()
    for _ in range(6):
        board = board.play(0)
    assert 0 not in board.legal_moves()


def test_ai_takes_immediate_win() -> None:
    cells = [0] * 42
    cells[5 * 7 + 0] = 1
    cells[5 * 7 + 1] = 1
    cells[5 * 7 + 2] = 1
    board = Board(tuple(cells), 1)
    assert choose_move(board, simulations=10, seed=1) == 3


def test_ai_blocks_immediate_loss() -> None:
    cells = [0] * 42
    cells[5 * 7 + 0] = -1
    cells[5 * 7 + 1] = -1
    cells[5 * 7 + 2] = -1
    board = Board(tuple(cells), 1)
    assert choose_move(board, simulations=10, seed=1) == 3
