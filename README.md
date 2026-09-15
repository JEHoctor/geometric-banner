# geometric-banner

Make geometric banner images, e.g. for a LinkedIn profile banner.

[According to LinkedIn](https://www.linkedin.com/help/linkedin/answer/70781/image-specifications-for-your-linkedin-pages-and-career-pages?lang=en), the optimal size for a profile banner is 1128 by 191 pixels. According to me, the best shape is the hexagon.

## Sample results

![sample hexagon tiling from this script](https://raw.githubusercontent.com/JEHoctor/geometric-banner/master/samples/geometric_banner.png)

![sample triangle tiling from this script](https://raw.githubusercontent.com/JEHoctor/geometric-banner/master/samples/triangles.png)

![sample Gaussian process pattern from this script](https://raw.githubusercontent.com/JEHoctor/geometric-banner/master/samples/gaussian_process.png)

## Usage

Run it without installing anything, using [uv](https://docs.astral.sh/uv/):

```
uvx geometric-banner
```

Or install it as a tool so `geometric-banner` is always on your `PATH`:

```
uv tool install geometric-banner
geometric-banner
```

(`pip install geometric-banner` works too.) Either way, the command writes
`geometric_banner.svg` and `geometric_banner.png` to the current directory.

Everything is optional; the defaults produce a LinkedIn-sized hexagon banner colored
by a Gaussian process in viridis. Pass `--seed` to make a result reproducible — with the
same installed versions of numpy and scikit-learn, that is; the Gaussian process sampler
goes through floating-point linear algebra, so upgrading those can shift the result slightly.

```
geometric-banner --shape triangle --colormap magma --seed 42
```

| Option | Values | Default |
|---|---|---|
| `--shape` | `hexagon`, `triangle` | `hexagon` |
| `--pattern` | `gaussian_process`, `random` | `gaussian_process` |
| `--colormap` | `viridis`, `magma`, `inferno`, `plasma` | `viridis` |
| `--seed` | any integer | none (a fresh random result each run) |
| `--scale` | shape size in pixels | `10` |
| `--padding-factor` | center-to-center spacing as a multiple of scale; below `1` the shapes overlap | `1.1` |
| `--width`, `--height` | canvas size in pixels | `1128`, `191` |

`geometric-banner --help` lists the same options.

## Development

Requires [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/).

```
just sync    # create the virtualenv and install everything
just check   # lint, format check, type check, and tests with coverage
just help    # list every recipe
```
