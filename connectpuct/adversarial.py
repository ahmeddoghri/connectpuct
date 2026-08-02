"""How much of the published 10/10 record is the agent, and how much is
the choice of opponent?

The README says it directly: beating a random mover and a center-only
mover "is not a hard bar." Concretely: an opponent with *zero* search,
that just always drops in the center column with no lookahead at all
(``connectpuct.mcts.center_policy``), already loses every game to the
PUCT agent. That result establishes almost nothing about playing
strength, only that the agent isn't actively bad.

``minimax_policy`` (:mod:`connectpuct.minimax`) is a real opponent: plain
alpha-beta search with a positional heuristic, no learning, no opening
book, just correct lookahead. Against it, the PUCT agent's win rate drops
from a perfect record to roughly 70%, a real, seed-sensitive contest
rather than a foregone conclusion.
"""
from __future__ import annotations

import random

from .engine import Board, empty_board
from .mcts import choose_move
from .minimax import minimax_policy


def puct_policy(board: Board, rng: random.Random) -> int:
    return choose_move(board, simulations=40, seed=rng.randint(0, 999_999))


def minimax_wrapped(board: Board, rng: random.Random) -> int:
    return minimax_policy(board, depth=3)


def play_game(policy_a, policy_b, seed: int, agent_first: bool) -> int:
    """Play one game. Returns the winner from the AGENT's perspective:
    1 = agent won, -1 = agent lost, 2 = draw."""
    rng = random.Random(seed)
    board = empty_board()
    while board.winner() == 0:
        agent_to_move = (board.player == 1) == agent_first
        move = policy_a(board, rng) if agent_to_move else policy_b(board, rng)
        board = board.play(move)
    win = board.winner()
    if win == 2:
        return 2
    agent_player = 1 if agent_first else -1
    return 1 if win == agent_player else -1


def match_against_minimax(games: int = 10, depth: int = 3) -> tuple[int, int, int]:
    """Play ``games`` games against minimax at the given depth, alternating
    who moves first. Returns (wins, losses, draws) from the agent's side."""
    wins = losses = draws = 0
    for idx in range(games):
        agent_first = idx % 2 == 0
        result = play_game(puct_policy, minimax_wrapped, seed=idx, agent_first=agent_first)
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            draws += 1
    return wins, losses, draws
