# SPDX-License-Identifier: AGPL-3.0-or-later
from typing import TypedDict

import pytest

from geometric_banner.shape import Hexagon, Triangle


class Canvas(TypedDict):
    scale: float
    padding_factor: float
    out_width: int
    out_height: int


@pytest.fixture
def small_canvas() -> Canvas:
    return {"scale": 10.0, "padding_factor": 1.1, "out_width": 100, "out_height": 50}


class TestHexagon:
    def test_instantiation(self, small_canvas: Canvas) -> None:
        h = Hexagon(**small_canvas)
        assert h.scale == small_canvas["scale"]
        assert h.out_width == small_canvas["out_width"]
        assert h.out_height == small_canvas["out_height"]

    def test_generates_polygons(self, small_canvas: Canvas) -> None:
        shapes = list(Hexagon(**small_canvas)())
        assert len(shapes) > 0

    def test_each_polygon_has_six_vertices(self, small_canvas: Canvas) -> None:
        shapes = list(Hexagon(**small_canvas)())
        for polygon in shapes:
            assert len(polygon) == 6

    def test_vertices_are_2d(self, small_canvas: Canvas) -> None:
        shapes = list(Hexagon(**small_canvas)())
        for polygon in shapes:
            for vertex in polygon:
                assert len(vertex) == 2


class TestTriangle:
    def test_instantiation(self, small_canvas: Canvas) -> None:
        t = Triangle(**small_canvas)
        assert t.scale == small_canvas["scale"]
        assert t.out_width == small_canvas["out_width"]
        assert t.out_height == small_canvas["out_height"]

    def test_generates_polygons(self, small_canvas: Canvas) -> None:
        shapes = list(Triangle(**small_canvas)())
        assert len(shapes) > 0

    def test_each_polygon_has_three_vertices(self, small_canvas: Canvas) -> None:
        shapes = list(Triangle(**small_canvas)())
        for polygon in shapes:
            assert len(polygon) == 3

    def test_vertices_are_2d(self, small_canvas: Canvas) -> None:
        shapes = list(Triangle(**small_canvas)())
        for polygon in shapes:
            for vertex in polygon:
                assert len(vertex) == 2

    def test_more_shapes_for_larger_canvas(self, small_canvas: Canvas) -> None:
        small = list(Triangle(**small_canvas)())
        large_canvas = small_canvas.copy()
        large_canvas["out_width"] = 200
        large_canvas["out_height"] = 100
        large = list(Triangle(**large_canvas)())
        assert len(large) > len(small)
