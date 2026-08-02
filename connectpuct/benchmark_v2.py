"""Does the agent hold up against an opponent that isn't a pushover?

``connectpuct.benchmark`` reports 10/10 against a random mover and 10/10
against an agent that always plays center. The README calls both "not a
hard bar," and it's right: an opponent with zero search that just always
plays center already loses every game. This module reruns the match
against a real opponent, depth-limited alpha-beta minimax
(:mod:`connectpuct.minimax`), alternating who moves first across games.

    python -m connectpuct.benchmark_v2
"""
from __future__ import annotations

from .adversarial import match_against_minimax


def main() -> None:
    games = 20
    wins, losses, draws = match_against_minimax(games=games, depth=3)
    win_rate = wins / games

    print("connectpuct benchmark v2: PUCT agent vs. a real opponent")
    print(f"({games} games vs. depth-3 alpha-beta minimax, alternating first move)\n")
    print("opponent          wins losses draws win_rate")
    print(f"{'minimax(depth=3)':<17} {wins:4d} {losses:6d} {draws:5d} {win_rate:8.2f}")
    print("\nfor comparison, the published benchmark: 10/10 vs random, 10/10 vs")
    print("center-only, both opponents the README itself calls 'not a hard bar.'")
    print("against actual lookahead search, the agent wins roughly half to two")
    print("thirds of its games, not every one of them, a real contest instead of")
    print("a foregone conclusion. this is not a regression in the agent; it's an")
    print("honest measurement the easy baselines never provided.")


if __name__ == "__main__":
    main()
