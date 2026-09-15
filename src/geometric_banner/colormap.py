# SPDX-License-Identifier: AGPL-3.0-or-later

"""Colormap lookup over the tables in :mod:`geometric_banner.colormap_data`."""

from geometric_banner.colormap_data import INFERNO, MAGMA, PLASMA, VIRIDIS

RGB = tuple[int, int, int]

COLORMAPS: dict[str, tuple[RGB, ...]] = {
    "viridis": VIRIDIS,
    "magma": MAGMA,
    "inferno": INFERNO,
    "plasma": PLASMA,
}


def lookup(table: tuple[RGB, ...], x: float) -> RGB:
    """Map ``x`` in [0, 1] to an entry of ``table``, matching matplotlib's lookup exactly."""
    if not 0 <= x <= 1:
        msg = "can only convert values in [0, 1] to colors"
        raise ValueError(msg)
    return table[min(int(x * len(table)), len(table) - 1)]
