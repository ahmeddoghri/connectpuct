from __future__ import annotations

from dataclasses import dataclass

ROWS = 6
COLS = 7
WIN_LINES = []
for r in range(ROWS):
    for c in range(COLS):
        if c <= COLS - 4:
            WIN_LINES.append(tuple((r, c + i) for i in range(4)))
        if r <= ROWS - 4:
            WIN_LINES.append(tuple((r + i, c) for i in range(4)))
        if r <= ROWS - 4 and c <= COLS - 4:
            WIN_LINES.append(tuple((r + i, c + i) for i in range(4)))
        if r >= 3 and c <= COLS - 4:
            WIN_LINES.append(tuple((r - i, c + i) for i in range(4)))


@dataclass(frozen=True)
class Board:
    cells: tuple[int, ...]
    player: int = 1

    def legal_moves(self) -> list[int]:
        return [c for c in range(COLS) if self.cells[c] == 0]

    def play(self, col: int) -> "Board":
        if col not in self.legal_moves():
            raise ValueError(f"illegal move: {col}")
        cells = list(self.cells)
        for row in range(ROWS - 1, -1, -1):
            idx = row * COLS + col
            if cells[idx] == 0:
                cells[idx] = self.player
                break
        return Board(tuple(cells), -self.player)

    def winner(self) -> int:
        for line in WIN_LINES:
            values = [self.cells[r * COLS + c] for r, c in line]
            if values[0] != 0 and values.count(values[0]) == 4:
                return values[0]
        if not self.legal_moves():
            return 2
        return 0


def empty_board() -> Board:
    return Board((0,) * (ROWS * COLS), 1)
