# SPDX-License-Identifier: AGPL-3.0-or-later

"""Manage the tilings."""

import abc
from collections.abc import Iterator
from math import cos, pi, sin, sqrt

import numpy as np
import numpy.typing as npt
from numpy.linalg import matrix_power


def rot_matrix(theta: float) -> npt.NDArray[np.float64]:
    return np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])


class Shape(abc.ABC):
    def __init__(
        self,
        scale: float,
        padding_factor: float,
        out_width: int,
        out_height: int,
    ) -> None:
        self.scale = scale
        self.padding_factor = padding_factor
        self.out_width = out_width
        self.out_height = out_height

    def __call__(self) -> Iterator[list[tuple[float, float]]]:
        """Generate polygons of the image."""
        scale = self.scale
        for vertices in self.generate_units():
            yield [(x * scale, y * scale) for x, y in vertices]

    @abc.abstractmethod
    def generate_units(self) -> Iterator[list[tuple[float, float]]]:
        """Generate unit polygons."""
        ...


class Hexagon(Shape):
    def generate_units(self) -> Iterator[list[tuple[float, float]]]:
        """Generate hexagons one unit wide."""
        rot60 = rot_matrix(pi / 3)
        placement_wrt_s = self.padding_factor * np.array([1, 0])
        placement_wrt_t = rot60 @ placement_wrt_s
        units = self.scale * self.padding_factor
        y_start = 0
        y_end = 1 + int(self.out_height / units * 2 / sqrt(3))
        x_start = int(-y_end / 2)
        x_end = 1 + int(self.out_width / units)
        for s in range(x_start, x_end):
            for t in range(y_start, y_end):
                base_p = placement_wrt_s * s + placement_wrt_t * t
                offset = np.array([0.5, 0.5 / sqrt(3)])
                yield [base_p + matrix_power(rot60, i) @ offset for i in range(6)]


class Triangle(Shape):
    def generate_units(self) -> Iterator[list[tuple[float, float]]]:
        """Generate triangles of side length one unit."""
        rot60 = rot_matrix(pi / 3)
        rot120 = rot_matrix(2 * pi / 3)
        placement_wrt_s = self.padding_factor * np.array([1, 0])
        placement_wrt_t = self.padding_factor * np.array([0, sqrt(3) / 2])
        units = self.scale * self.padding_factor
        x_end = self.out_width / units
        y_end = self.out_height / units * 2 / sqrt(3)
        for t in range(2 + int(y_end)):
            for s_int in range(2 + int(x_end)):
                s = s_int if t % 2 else s_int - 0.5  # horizontal offset on odd rows

                base_p = placement_wrt_s * s + placement_wrt_t * t
                offset = np.array([0.5, 0.5 / sqrt(3)])
                yield [base_p + matrix_power(rot120, i) @ offset for i in range(3)]

                base_p += self.padding_factor * np.array([0.5, 1 / sqrt(3) - sqrt(3) / 2])
                offset = rot60 @ offset
                yield [base_p + matrix_power(rot120, i) @ offset for i in range(3)]
