import xml.etree.ElementTree as ET
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Literal

import numpy as np
import rich
import typer
from cairosvg import svg2png

from geometric_banner.colormap import viridis
from geometric_banner.pattern_generators import gaussian_process_pattern, random_pattern
from geometric_banner.shape import Hexagon, Shape, Triangle

app = typer.Typer()

SHAPES: dict[str, type[Shape]] = {"hexagon": Hexagon, "triangle": Triangle}
PATTERNS: dict[str, Callable] = {"gaussian_process": gaussian_process_pattern, "random": random_pattern}

# locations for output files
here = Path()
out_svg = here / "geometric_banner.svg"
out_png = here / "geometric_banner.png"


def get_color(x: float) -> str:
    return f"rgb{viridis(x)}"


@app.command()
def main(
    shape: Annotated[Literal["hexagon", "triangle"], typer.Option(help="Shape to tile across the banner")] = "hexagon",
    pattern: Annotated[
        Literal["gaussian_process", "random"], typer.Option(help="Color pattern to apply")
    ] = "gaussian_process",
    scale: Annotated[float, typer.Option(help="Shape scale in pixels")] = 10.0,
    padding_factor: Annotated[float, typer.Option(help="Padding between shapes")] = 1.1,
    width: Annotated[int, typer.Option(help="Canvas width in pixels")] = 1128,
    height: Annotated[int, typer.Option(help="Canvas height in pixels")] = 191,
) -> None:
    _main(SHAPES[shape](scale, padding_factor, width, height), PATTERNS[pattern])
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
    for vertices, color in zip(shapes, colors, strict=True):
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
