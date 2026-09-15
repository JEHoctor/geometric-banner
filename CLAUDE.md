# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`geometric-banner` is a small Python CLI (published on PyPI, AGPL-3.0-or-later) that tiles
a canvas with hexagons or triangles, colors each tile from a Gaussian-process or random
field through a viridis-family colormap, and writes `geometric_banner.svg` + `.png` to the
**current working directory**. Default canvas is LinkedIn's 1128×191 banner size.

The `~/Projects/CLAUDE.md` handbook (loaded automatically) covers git identity, commit
trailers, the GitHub PAT, and the `gh pr create` workaround; this file is repo-specific.

## Commands

Tooling is `uv` + `just`; every recipe wraps `uv run`, so there is no venv to activate.

```
just sync            # uv sync --all-extras (dev extra: pytest, pytest-cov, ruff, ty)
just check           # lint + format-check + typecheck + test — same steps as CI
just lint            # ruff check src/ tests/
just format          # ruff format src/ tests/   (format-check to verify only)
just typecheck       # ty check src/ tests/
just test            # pytest -vv (coverage is in pyproject addopts)

uv run pytest tests/test_shape.py                    # one file
uv run pytest tests/test_main.py -k same_seed        # one test by name
uv run pytest -m licensing                           # only the SPDX header tests
uv run geometric-banner --seed 0 --width 60 --height 20   # run the CLI from source
```

CI (`.github/workflows/ci.yml`) runs `just check`'s steps on Python 3.11–3.13, plus a
`lowest` job: `uv run --isolated --resolution lowest-direct --all-extras pytest`. Any
bump to a floor in `pyproject.toml` `dependencies` must keep that job green — each floor
has a comment explaining why it was chosen; keep that convention.

Releases: bump `version` in `pyproject.toml`, merge, publish a GitHub release;
`publish.yml` builds with `uv build` and uploads via PyPI Trusted Publishing.

## Architecture

The pipeline in `src/geometric_banner/main.py::_main` is: **Shape → sample points →
Pattern → Colormap → SVG → PNG**.

- `shape.py` — `Shape` ABC. Subclasses implement `generate_units()` yielding polygons in
  *unit* coordinates (side/width 1); `Shape.__call__` multiplies by `scale`. Tilings are
  built with rotation matrices (`rot_matrix`, `matrix_power`) rather than hard-coded
  vertices, and deliberately overshoot the canvas (negative start indices, `+1`/`+2`
  ranges) so edges are covered. `padding_factor` is center-to-center spacing in units;
  `< 1` overlaps.
- `pattern_generators.py` — a `Pattern` is `Callable[[FloatArray, int | None], FloatArray]`:
  takes the N×2 array of polygon centroids and an optional seed, returns N values in
  `[0, 1]`. `gaussian_process_pattern` samples a fixed-length-scale Matérn GP via
  scikit-learn and min-max normalizes; results are seed-reproducible only for a fixed
  numpy/scikit-learn version (floating-point linear algebra).
- `colormap.py` / `colormap_data.py` — `lookup(table, x)` reproduces matplotlib's
  integer-index lookup exactly. `colormap_data.py` is the vendored 256-entry viridis,
  magma, inferno, plasma tables (CC0, captured from matplotlib 3.11.2 with
  `cmap(x, bytes=True)`); matplotlib is *not* a dependency. `test_colormap.py` checks the
  tables against those captured values.
- `main.py` — the typer app. Option choices are `Literal[...]` types (needs typer ≥ 0.19)
  mapped through the `SHAPES` / `PATTERNS` / `COLORMAPS` dicts; adding a shape, pattern
  or colormap means adding to both the `Literal` and the dict. Output paths are
  module-level constants relative to cwd, which is why `tests/test_main.py` uses a
  `monkeypatch.chdir(tmp_path)` fixture.

## Conventions enforced by the test suite / linters

- **SPDX headers**: every `.py` under `src/` and `tests/` must start with
  `# SPDX-License-Identifier: AGPL-3.0-or-later`. Files under a different licence are
  listed in `[tool.geometric-banner.license-exceptions]` in `pyproject.toml`
  (currently only `colormap_data.py` = `CC0-1.0`); `tests/test_licensing.py` and ruff's
  `flake8-copyright` rule both check this. A new file without the header fails CI.
- ruff runs with `select = ["ALL"]`, line length 120, Google docstring convention; the
  ignore list in `pyproject.toml` is short and each entry is justified in a comment —
  add a new ignore the same way rather than sprinkling `# noqa`. Tests are type-annotated
  on purpose (ANN is enforced there) so `ty` has something to check.
- `.claude/worktrees/` is a git worktree directory, not source; exclude it from searches.
