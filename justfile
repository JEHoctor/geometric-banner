# Default: list recipes
default:
    @just --list

# Install / sync dependencies with uv
sync:
    uv sync --all-extras

# Lint with ruff
lint:
    uv run ruff check src/ tests/

# Format with ruff
format:
    uv run ruff format src/ tests/

# Type-check with ty
typecheck:
    uv run ty check src/

# Run tests with pytest
test:
    uv run pytest -vv

# Run all checks (lint + typecheck + test)
check: lint typecheck test

# Build distribution
build:
    uv build

# Publish to PyPI
publish:
    uv publish
