# connectpuct

A Connect Four AI that actually has to play the game, in a browser, against you, instead of just printing a win rate and hoping you believe it.

![python](https://img.shields.io/badge/python-3.9%2B-blue)
![deps](https://img.shields.io/badge/runtime%20deps-none-success)
![license](https://img.shields.io/badge/license-MIT-black)

Every game AI repo has a benchmark table. Very few of them let you actually
sit down and lose to the thing. connectpuct ships both: a PUCT-style Monte
Carlo tree search agent in Python with tactical priors for center control,
immediate wins, and blocks, plus a dependency-free browser game at
`web/index.html` you can open and get humbled by in under a minute.

## Run it

```bash
git clone https://github.com/ahmeddoghri/connectpuct
cd connectpuct
pip install -e ".[dev]"
python -m connectpuct.benchmark
```

Then open `web/index.html` to play it yourself. No server, no build step, no
excuse not to.

## Verified benchmark

Generated locally with `python -m connectpuct.benchmark`:

```text
opponent    wins losses draws win_rate
random      10      0     0    1.00
center      10      0     0    1.00
```

Ten out of ten against a random mover and ten out of ten against an agent
that just grabs the center column. Neither of those is a hard bar, which is
exactly the point. A search agent that cannot clear it has no business
calling itself an agent.

**Update:** I took "neither of those is a hard bar" at its word and built
a real opponent to check. Against depth-3 alpha-beta minimax, no
learning, just correct lookahead, the win rate drops from a perfect
record to roughly 55%: a real contest, not a foregone conclusion.
`python -m connectpuct.benchmark_v2`. Details below.

## What happens against an opponent that isn't a pushover

The README already said the quiet part out loud: beating random and
center-only "is not a hard bar." Here's how weak that bar actually is:
`center_policy` has zero search, no MCTS, no lookahead at all, it just
always plays the center column, and it already beats the random baseline
almost every game on its own. A 10/10 record against random or center
says the agent isn't actively broken. It says nothing about how strong it
is.

`connectpuct/minimax.py` adds a real opponent: depth-limited alpha-beta
minimax with a center-weighted positional heuristic, no learning, no
opening book, just correct lookahead a fixed number of plies deep, the
standard first thing anyone building a game AI reaches for to sanity-check
real strength.

```bash
python -m connectpuct.benchmark_v2
```
```
opponent          wins losses draws win_rate
minimax(depth=3)    11      9     0     0.55
```

20 games, alternating who moves first each game. The record against a
real opponent is close to even, not the sweep the published numbers
imply. This isn't a regression or a bug: the PUCT agent, `mcts.py`, and
the published 10/10-vs-random/center numbers are all untouched and still
reproduce exactly. It's the honest measurement the easy baselines never
provided, and it's a genuinely useful number if you're deciding whether
to trust this agent for anything beyond beating an opponent that plays
the same column every turn.

## Research trail

- OpenSpiel, active game AI benchmark library: https://github.com/google-deepmind/open_spiel
- Speculative Monte Carlo Tree Search, 2024: https://proceedings.neurips.cc/paper_files/paper/2024/file/a19940b01b77b6acd41ff8b32b334e7c-Paper-Conference.pdf
- MCTX JAX Monte Carlo tree search, active OSS: https://github.com/google-deepmind/mctx
- Game AI and procedural content generation benchmark work, 2025: https://arxiv.org/abs/2502.06457

## Tests

```bash
pytest -q
ruff check .
```

MIT © Ahmed Doghri
