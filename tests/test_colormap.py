import pytest

from geometric_banner.colormap import COLORMAPS, INFERNO, MAGMA, PLASMA, RGB, VIRIDIS, lookup


def test_four_colormaps_registered() -> None:
    assert set(COLORMAPS) == {"viridis", "magma", "inferno", "plasma"}


@pytest.mark.parametrize("name", sorted(COLORMAPS))
def test_table_has_256_entries(name: str) -> None:
    assert len(COLORMAPS[name]) == 256


# Anchor values captured from matplotlib 3.11.2 via cmap(x, bytes=True).
@pytest.mark.parametrize(
    ("table", "x", "expected"),
    [
        (VIRIDIS, 0.0, (68, 1, 84)),
        (VIRIDIS, 0.5, (32, 144, 140)),
        (VIRIDIS, 1.0, (253, 231, 36)),
        (MAGMA, 0.0, (0, 0, 3)),
        (MAGMA, 0.5, (182, 54, 121)),
        (MAGMA, 1.0, (251, 252, 191)),
        (INFERNO, 0.0, (0, 0, 3)),
        (INFERNO, 0.5, (187, 55, 84)),
        (INFERNO, 1.0, (252, 254, 164)),
        (PLASMA, 0.0, (12, 7, 134)),
        (PLASMA, 0.5, (203, 71, 119)),
        (PLASMA, 1.0, (239, 248, 33)),
    ],
)
def test_matches_matplotlib_anchor_values(table: tuple[RGB, ...], x: float, expected: RGB) -> None:
    assert lookup(table, x) == expected


def test_top_of_range_maps_to_last_entry() -> None:
    assert lookup(VIRIDIS, 1.0) == VIRIDIS[-1]
    assert lookup(VIRIDIS, 0.999) == VIRIDIS[-1]


@pytest.mark.parametrize("x", [-0.01, 1.01])
def test_rejects_out_of_range(x: float) -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        lookup(VIRIDIS, x)
