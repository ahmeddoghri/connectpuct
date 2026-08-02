"""A depth-limited alpha-beta minimax opponent: a genuinely competent test.

The bundled benchmark's own README says it plainly: beating a random mover
and an agent that always plays center "is not a hard bar." Both baselines
lose to almost any coherent strategy, including one that just always
grabs the center column with no search at all (see
:mod:`connectpuct.adversarial`). Neither result says anything about how
strong the PUCT agent actually is.

This module is a plain depth-limited minimax with alpha-beta pruning and a
simple center-weighted positional heuristic, the standard first opponent
anyone building a game AI reaches for to sanity-check real strength. It
has no learned weights, no opening book, nothing fancy: just correct
lookahead a fixed number of plies deep.
"""
from __future__ import annotations

from .engine import COLS, ROWS, Board


def _heuristic(board: Board, root_player: int) -> int:
    score = 0
    for col in range(COLS):
        for row in range(ROWS):
            value = board.cells[row * COLS + col]
            weight = 3 - abs(3 - col)
            if value == root_player:
                score += weight
            elif value == -root_player:
                score -= weight
    return score


def _minimax(board: Board, depth: int, alpha: float, beta: float, root_player: int) -> float:
    win = board.winner()
    if win == root_player:
        return 1000 + depth
    if win == -root_player:
        return -1000 - depth
    if win == 2:
        return 0
    if depth == 0:
        return _heuristic(board, root_player)

    maximizing = board.player == root_player
    legal = board.legal_moves()
    if maximizing:
        value = float("-inf")
        for move in legal:
            value = max(value, _minimax(board.play(move), depth - 1, alpha, beta, root_player))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    value = float("inf")
    for move in legal:
        value = min(value, _minimax(board.play(move), depth - 1, alpha, beta, root_player))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value


def minimax_policy(board: Board, depth: int = 3) -> int:
    """Pick the move that looks best ``depth`` plies ahead, with alpha-beta
    pruning. Ties broken by move order (leftmost of the best-scoring)."""
    root_player = board.player
    best_move, best_value = board.legal_moves()[0], float("-inf")
    for move in board.legal_moves():
        value = _minimax(board.play(move), depth - 1, float("-inf"), float("inf"), root_player)
        if value > best_value:
            best_value, best_move = value, move
    return best_move
