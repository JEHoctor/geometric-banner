# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Callable

import numpy as np
import pytest

from geometric_banner.pattern_generators import FloatArray, gaussian_process_pattern, random_pattern

Pattern = Callable[..., FloatArray]
PATTERNS: list[Pattern] = [random_pattern, gaussian_process_pattern]


@pytest.fixture
def sample_points() -> FloatArray:
    rng = np.random.default_rng(42)
    return rng.uniform(0, 100, size=(20, 2))


@pytest.mark.parametrize("pattern", PATTERNS)
class TestPattern:
    @pytest.mark.parametrize("seed", [0, None])
    def test_returns_correct_length(self, pattern: Pattern, sample_points: FloatArray, seed: int | None) -> None:
        assert len(pattern(sample_points, seed=seed)) == len(sample_points)

    @pytest.mark.parametrize("seed", [0, None])
    def test_values_in_unit_interval(self, pattern: Pattern, sample_points: FloatArray, seed: int | None) -> None:
        result = pattern(sample_points, seed=seed)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)

    def test_same_seed_is_reproducible(self, pattern: Pattern, sample_points: FloatArray) -> None:
        np.testing.assert_array_equal(pattern(sample_points, seed=7), pattern(sample_points, seed=7))

    def test_different_seeds_differ(self, pattern: Pattern, sample_points: FloatArray) -> None:
        assert not np.array_equal(pattern(sample_points, seed=1), pattern(sample_points, seed=2))
