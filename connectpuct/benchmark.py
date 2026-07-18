from __future__ import annotations

import random

from .engine import Board, empty_board
from .mcts import center_policy, choose_move, random_policy


def play_game(policy_a, policy_b, seed: int) -> int:
    rng = random.Random(seed)
    board = empty_board()
    while board.winner() == 0:
        if board.player == 1:
            move = policy_a(board, rng)
        else:
            move = policy_b(board, rng)
        board = board.play(move)
    return board.winner()


def puct_policy(board: Board, rng: random.Random) -> int:
    return choose_move(board, simulations=40, seed=rng.randint(0, 999_999))


def random_wrapped(board: Board, rng: random.Random) -> int:
    return random_policy(board, rng)


def center_wrapped(board: Board, rng: random.Random) -> int:
    return center_policy(board)


def match(policy_a, policy_b, games: int = 10) -> tuple[int, int, int]:
    wins = losses = draws = 0
    for idx in range(games):
        result = play_game(policy_a, policy_b, idx)
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            draws += 1
    return wins, losses, draws


def main() -> None:
    vs_random = match(puct_policy, random_wrapped)
    vs_center = match(puct_policy, center_wrapped)
    print("connectpuct benchmark: PUCT Connect Four agent")
    print("opponent    wins losses draws win_rate")
    for label, row in [("random", vs_random), ("center", vs_center)]:
        wins, losses, draws = row
        print(f"{label:9s} {wins:4d} {losses:6d} {draws:5d} {wins / sum(row):7.2f}")
    print("playable    web/index.html")


if __name__ == "__main__":
    main()
