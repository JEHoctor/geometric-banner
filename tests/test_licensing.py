# SPDX-License-Identifier: AGPL-3.0-or-later

"""Every Python file declares AGPL unless pyproject.toml lists it as an exception."""

import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROJECT_LICENSE = "AGPL-3.0-or-later"
SPDX_LINE = re.compile(r"^# SPDX-License-Identifier: (?P<id>\S+)$", re.MULTILINE)

PYTHON_FILES = sorted(p.relative_to(ROOT) for d in ("src", "tests") for p in (ROOT / d).rglob("*.py"))
EXCEPTIONS: dict[str, str] = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]["geometric-banner"][
    "license-exceptions"
]


def spdx_identifier(path: Path) -> str | None:
    match = SPDX_LINE.search((ROOT / path).read_text(), endpos=1024)
    return match["id"] if match else None


@pytest.mark.licensing
@pytest.mark.parametrize("path", PYTHON_FILES, ids=str)
def test_file_declares_expected_license(path: Path) -> None:
    expected = EXCEPTIONS.get(path.as_posix(), PROJECT_LICENSE)
    assert spdx_identifier(path) == expected, (
        f"{path} should declare {expected}; to license a file differently, list it under "
        "[tool.geometric-banner.license-exceptions] in pyproject.toml"
    )


@pytest.mark.licensing
@pytest.mark.parametrize("path", sorted(EXCEPTIONS), ids=str)
def test_exception_refers_to_existing_file(path: str) -> None:
    assert (ROOT / path).is_file(), f"stale license exception: {path} does not exist"
