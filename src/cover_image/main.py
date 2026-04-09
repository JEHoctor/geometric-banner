# standard libraries
import xml.etree.ElementTree as ET
from collections.abc import Callable
from enum import StrEnum
from pathlib import Path
from typing import Annotated

# third party libraries
import numpy as np
import rich
import typer
from cairosvg import svg2png
from matplotlib import colormaps

# cover image libraries
from cover_image.pattern_generators import gaussian_process_pattern, random_pattern
from cover_image.shape import Hexagon, Shape, Triangle

app = typer.Typer()

_name_to_shape: dict[str, type[Shape]] = {s.__name__: s for s in (Hexagon, Triangle)}
_name_to_pattern = {"gaussian_process": gaussian_process_pattern, "random": random_pattern}

# locations for output files
here = Path()
out_svg = here / "cover_image.svg"
out_png = here / "cover_image.png"

# basic static result properties
colormap = colormaps.get_cmap("viridis")


class ShapeChoice(StrEnum):
    Hexagon = "Hexagon"
    Triangle = "Triangle"


class PatternChoice(StrEnum):
    gaussian_process = "gaussian_process"
    random = "random"


def get_color(x: float) -> str:
    if not (0 <= x <= 1):
        raise ValueError("can only convert values in [0, 1] to colors")
    color_bytes = tuple(map(int, colormap(x, bytes=True)[:3]))
    return f"rgb{color_bytes}"


@app.command()
def main(
    shape: Annotated[ShapeChoice, typer.Option(help="Shape to tile across the banner")] = ShapeChoice.Hexagon,
    pattern: Annotated[PatternChoice, typer.Option(help="Color pattern to apply")] = PatternChoice.gaussian_process,
    scale: Annotated[float, typer.Option(help="Shape scale in pixels")] = 10.0,
    padding_factor: Annotated[float, typer.Option(help="Padding between shapes")] = 1.1,
    width: Annotated[int, typer.Option(help="Canvas width in pixels")] = 1128,
    height: Annotated[int, typer.Option(help="Canvas height in pixels")] = 191,
) -> None:
    shape_cls = _name_to_shape[shape.value]
    shape_obj = shape_cls(scale, padding_factor, width, height)
    pattern_fn = _name_to_pattern[pattern.value]
    _main(shape_obj, pattern_fn)
    rich.print(f"[green]✓[/green] Saved {out_svg} and {out_png}")


def _main(shape: Shape, pattern: Callable) -> None:
    # Initialize a blank canvas of the right size.
    svg_root = ET.Element("svg", attrib={"viewBox": f"0 0 {shape.out_width} {shape.out_height}", "version": "1.1"})
    svg_image = ET.ElementTree(element=svg_root)

    # Add a black background.
    ET.SubElement(svg_root, "rect", attrib={"width": "100%", "height": "100%", "fill": "black"})

    # Find a color for each shape.
    shapes = list(shape())
    sample_points = np.vstack([np.mean(s, axis=0) for s in shapes])
    colors = [get_color(v) for v in pattern(sample_points)]

    # Add the shapes.
    for vertices, color in zip(shapes, colors):
        ET.SubElement(
            svg_root,
            "polygon",
            attrib={"points": " ".join(f"{x},{y}" for x, y in vertices), "fill": color},
        )

    # Write the result files.
    svg_image.write(
        out_svg,
        encoding="UTF-8",
        xml_declaration=True,
    )
    svg2png(url=str(out_svg), write_to=str(out_png))


if __name__ == "__main__":
    app()
