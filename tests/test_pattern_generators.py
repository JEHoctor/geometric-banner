import numpy as np
import pytest

from geometric_banner.pattern_generators import FloatArray, gaussian_process_pattern, random_pattern


@pytest.fixture
def sample_points() -> FloatArray:
    rng = np.random.default_rng(42)
    return rng.uniform(0, 100, size=(20, 2))


class TestRandomPattern:
    def test_returns_correct_length(self, sample_points: FloatArray) -> None:
        result = random_pattern(sample_points)
        assert len(result) == len(sample_points)

    def test_values_in_unit_interval(self, sample_points: FloatArray) -> None:
        result = random_pattern(sample_points)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)


class TestGaussianProcessPattern:
    def test_returns_correct_length(self, sample_points: FloatArray) -> None:
        rng = np.random.RandomState(0)
        result = gaussian_process_pattern(sample_points, random_state=rng)
        assert len(result) == len(sample_points)

    def test_values_in_unit_interval(self, sample_points: FloatArray) -> None:
        rng = np.random.RandomState(0)
        result = gaussian_process_pattern(sample_points, random_state=rng)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)

    def test_reproducible_with_same_seed(self, sample_points: FloatArray) -> None:
        result_a = gaussian_process_pattern(sample_points, random_state=np.random.RandomState(7))
        result_b = gaussian_process_pattern(sample_points, random_state=np.random.RandomState(7))
        np.testing.assert_array_equal(result_a, result_b)

    def test_different_seeds_differ(self, sample_points: FloatArray) -> None:
        result_a = gaussian_process_pattern(sample_points, random_state=np.random.RandomState(1))
        result_b = gaussian_process_pattern(sample_points, random_state=np.random.RandomState(2))
        assert not np.array_equal(result_a, result_b)
