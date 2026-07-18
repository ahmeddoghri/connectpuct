# connectpuct

A playable Connect Four repo with an AI opponent and a benchmarked search
agent. The Python agent uses PUCT-style Monte Carlo tree search with tactical
priors. The browser game is dependency-free and runs from `web/index.html`.

![CI](https://github.com/ahmeddoghri/connectpuct/actions/workflows/ci.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![deps](https://img.shields.io/badge/runtime%20deps-none-success)
![license](https://img.shields.io/badge/license-MIT-black)

## Run it

```bash
git clone https://github.com/ahmeddoghri/connectpuct
cd connectpuct
pip install -e ".[dev]"
python -m connectpuct.benchmark
```

Open `web/index.html` to play.

## Verified benchmark

These numbers were generated locally with `python -m connectpuct.benchmark`:

```text
opponent    wins losses draws win_rate
random      10      0     0    1.00
center      10      0     0    1.00
```

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
