from importlib.metadata import version
from pathlib import Path

import pytest
from typer.testing import CliRunner

from geometric_banner.main import app

runner = CliRunner()
SMALL = ["--width", "60", "--height", "20"]


@pytest.fixture
def cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Run the CLI in an empty temporary directory, since it writes to the cwd."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_run_writes_svg_and_png(cwd: Path) -> None:
    result = runner.invoke(app, [*SMALL, "--seed", "0"])
    assert result.exit_code == 0, result.output
    assert "Saved" in result.output
    assert (cwd / "geometric_banner.svg").is_file()
    assert (cwd / "geometric_banner.png").is_file()


def test_same_seed_gives_identical_svg(cwd: Path) -> None:
    assert runner.invoke(app, [*SMALL, "--seed", "0"]).exit_code == 0
    first = (cwd / "geometric_banner.svg").read_bytes()
    assert runner.invoke(app, [*SMALL, "--seed", "0"]).exit_code == 0
    assert (cwd / "geometric_banner.svg").read_bytes() == first


def test_different_seeds_give_different_svg(cwd: Path) -> None:
    assert runner.invoke(app, [*SMALL, "--seed", "1"]).exit_code == 0
    first = (cwd / "geometric_banner.svg").read_bytes()
    assert runner.invoke(app, [*SMALL, "--seed", "2"]).exit_code == 0
    assert (cwd / "geometric_banner.svg").read_bytes() != first


def test_invalid_shape_is_rejected() -> None:
    result = runner.invoke(app, ["--shape", "square"])
    assert result.exit_code != 0
    assert "square" in result.output


def test_colormap_option_changes_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    args = ["--seed", "0", "--width", "60", "--height", "20"]
    assert runner.invoke(app, [*args, "--colormap", "viridis"]).exit_code == 0
    viridis_svg = Path("geometric_banner.svg").read_bytes()
    assert runner.invoke(app, [*args, "--colormap", "magma"]).exit_code == 0
    magma_svg = Path("geometric_banner.svg").read_bytes()
    assert viridis_svg != magma_svg


def test_rejects_unknown_colormap() -> None:
    assert runner.invoke(app, ["--colormap", "jet"]).exit_code != 0


def test_version_flag_prints_version_and_exits(cwd: Path) -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == f"geometric-banner {version('geometric-banner')}"
    assert not (cwd / "geometric_banner.svg").exists()
