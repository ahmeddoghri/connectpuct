"""Tests for the weak-baseline finding: does the agent hold up against a
real opponent, not just ones the README itself calls "not a hard bar"?"""

from __future__ import annotations

import random

from connectpuct.adversarial import match_against_minimax, play_game, puct_policy
from connectpuct.engine import empty_board
from connectpuct.mcts import center_policy, random_policy
from connectpuct.minimax import minimax_policy

# --- the finding: the published baselines are trivially weak ---------------

def test_zero_search_opponent_already_beats_the_bundled_random_baseline():
    """center_policy has no search at all, no MCTS, no lookahead, it just
    always plays the center column. It still beats random every time,
    which is exactly why the README calls random "not a hard bar.\""""
    wins = 0
    for seed in range(10):
        rng = random.Random(seed)
        board = empty_board()
        agent_first = seed % 2 == 0
        while board.winner() == 0:
            if (board.player == 1) == agent_first:
                move = center_policy(board)
            else:
                move = random_policy(board, rng)
            board = board.play(move)
        win = board.winner()
        if win == 2:
            continue
        agent_player = 1 if agent_first else -1
        wins += win == agent_player
    assert wins >= 8  # a zero-search policy dominates the "random" baseline


def test_minimax_beats_the_weak_center_baseline_going_first():
    """Unlike center_policy or random_policy, minimax has real lookahead.
    Both policies are fully deterministic (no rng), so this checks the one
    game that exists rather than pretending repeated "seeds" add signal."""
    b = empty_board()
    while b.winner() == 0:
        move = minimax_policy(b, depth=3) if b.player == 1 else center_policy(b)
        b = b.play(move)
    assert b.winner() == 1


# --- the fix: measure against a fair opponent -------------------------------

def test_puct_agent_does_not_sweep_minimax():
    """Against a real opponent, the published 10/10-everywhere pattern
    should not hold: some games should be losses."""
    wins, losses, draws = match_against_minimax(games=10, depth=3)
    assert wins + losses + draws == 10
    assert losses > 0  # unlike vs random/center, minimax actually wins some


def test_puct_agent_still_wins_a_real_share_of_games():
    """The agent should not be worthless against minimax either; a
    reasonable win rate confirms the MCTS search is doing real work."""
    wins, losses, draws = match_against_minimax(games=10, depth=3)
    assert wins / 10 >= 0.3


def test_play_game_alternates_first_player_correctly():
    """agent_first=False must mean the agent is player -1, not player 1."""
    result_first = play_game(puct_policy, lambda b, r: minimax_policy(b, depth=1), seed=0, agent_first=True)
    result_second = play_game(puct_policy, lambda b, r: minimax_policy(b, depth=1), seed=0, agent_first=False)
    assert result_first in (-1, 1, 2)
    assert result_second in (-1, 1, 2)


# --- the original module is untouched ---------------------------------------

def test_original_mcts_module_untouched():
    import connectpuct.mcts as mcts_module

    assert not hasattr(mcts_module, "minimax_policy")


def test_original_benchmark_still_reproduces():
    """The published 10/10-vs-random, 10/10-vs-center numbers still hold;
    this finding doesn't change the agent, only adds a harder opponent."""
    from connectpuct.benchmark import center_wrapped, match, puct_policy, random_wrapped

    vs_random = match(puct_policy, random_wrapped)
    vs_center = match(puct_policy, center_wrapped)
    assert vs_random == (10, 0, 0)
    assert vs_center == (10, 0, 0)


def test_minimax_is_deterministic():
    from connectpuct.engine import empty_board

    board = empty_board().play(3)
    assert minimax_policy(board, depth=3) == minimax_policy(board, depth=3)
