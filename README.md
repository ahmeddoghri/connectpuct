# connectpuct

A Connect Four AI that actually has to play the game, in a browser, against you, instead of just printing a win rate and hoping you believe it.

![CI](https://github.com/ahmeddoghri/connectpuct/actions/workflows/ci.yml/badge.svg)
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
