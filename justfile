# List recipes
help:
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

# Check formatting without changing files
format-check:
    uv run ruff format --check src/ tests/

# Type-check with ty
typecheck:
    uv run ty check src/ tests/

# Run tests with pytest
test:
    uv run pytest -vv

# Run all checks (lint + format-check + typecheck + test)
check: lint format-check typecheck test
