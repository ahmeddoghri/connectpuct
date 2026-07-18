from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from .engine import Board


@dataclass
class Node:
    board: Board
    prior: float
    visits: int = 0
    value_sum: float = 0.0
    children: dict[int, "Node"] = field(default_factory=dict)

    @property
    def value(self) -> float:
        return 0.0 if self.visits == 0 else self.value_sum / self.visits


def _winning_move(board: Board, player: int) -> int | None:
    for move in board.legal_moves():
        nxt = board.play(move)
        if nxt.winner() == player:
            return move
    return None


def _priors(board: Board) -> dict[int, float]:
    legal = board.legal_moves()
    weights = {}
    for move in legal:
        weight = 1.0 + (3 - abs(3 - move)) * 0.45
        nxt = board.play(move)
        if nxt.winner() == board.player:
            weight += 8.0
        if _winning_move(nxt, nxt.player) is not None:
            weight -= 0.6
        weights[move] = max(0.05, weight)
    total = sum(weights.values())
    return {move: weight / total for move, weight in weights.items()}


def _rollout(board: Board, rng: random.Random) -> float:
    root_player = board.player
    state = board
    for _ in range(42):
        win = state.winner()
        if win == root_player:
            return 1.0
        if win == -root_player:
            return -1.0
        if win == 2:
            return 0.0
        immediate = _winning_move(state, state.player)
        if immediate is None:
            block = _winning_move(Board(state.cells, -state.player), -state.player)
            move = block if block in state.legal_moves() else rng.choice(state.legal_moves())
        else:
            move = immediate
        state = state.play(move)
    return 0.0


def _simulate(node: Node, rng: random.Random, c_puct: float) -> float:
    win = node.board.winner()
    if win:
        if win == 2:
            value = 0.0
        else:
            value = 1.0 if win == node.board.player else -1.0
        node.visits += 1
        node.value_sum += value
        return value

    if not node.children:
        for move, prior in _priors(node.board).items():
            node.children[move] = Node(node.board.play(move), prior)
        value = _rollout(node.board, rng)
        node.visits += 1
        node.value_sum += value
        return value

    best_move = None
    best_score = float("-inf")
    parent_sqrt = math.sqrt(max(1, node.visits))
    for move, child in node.children.items():
        score = -child.value + c_puct * child.prior * parent_sqrt / (1 + child.visits)
        if score > best_score:
            best_move = move
            best_score = score
    assert best_move is not None
    value = -_simulate(node.children[best_move], rng, c_puct)
    node.visits += 1
    node.value_sum += value
    return value


def choose_move(board: Board, simulations: int = 80, seed: int = 0, c_puct: float = 1.4) -> int:
    immediate = _winning_move(board, board.player)
    if immediate is not None:
        return immediate
    opponent_board = Board(board.cells, -board.player)
    block = _winning_move(opponent_board, -board.player)
    if block in board.legal_moves():
        return block
    rng = random.Random(seed)
    root = Node(board, 1.0)
    for _ in range(simulations):
        _simulate(root, rng, c_puct)
    if not root.children:
        return board.legal_moves()[0]
    return max(root.children.items(), key=lambda item: item[1].visits)[0]


def center_policy(board: Board) -> int:
    legal = board.legal_moves()
    return min(legal, key=lambda move: abs(3 - move))


def random_policy(board: Board, rng: random.Random) -> int:
    return rng.choice(board.legal_moves())
