import pytest

from geometric_banner.colormap import RGB, VIRIDIS, viridis


def test_table_has_256_entries() -> None:
    assert len(VIRIDIS) == 256


@pytest.mark.parametrize(
    ("x", "expected"),
    [
        (0.0, (68, 1, 84)),  # matplotlib viridis(0.0, bytes=True)
        (0.5, (32, 144, 140)),  # matplotlib viridis(0.5, bytes=True)
        (1.0, (253, 231, 36)),  # matplotlib viridis(1.0, bytes=True)
    ],
)
def test_matches_matplotlib_anchor_values(x: float, expected: RGB) -> None:
    assert viridis(x) == expected


def test_top_of_range_maps_to_last_entry() -> None:
    assert viridis(1.0) == VIRIDIS[-1]
    assert viridis(0.999) == VIRIDIS[-1]


@pytest.mark.parametrize("x", [-0.01, 1.01])
def test_rejects_out_of_range(x: float) -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        viridis(x)
