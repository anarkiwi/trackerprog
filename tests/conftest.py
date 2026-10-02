"""Shared fixtures for the tuneprog/trackerprog test suite.

``ctx6510`` compiles+installs deity-informant's 6510 SLEIGH module into a scratch
pypcode processors tree and returns a loaded ``pypcode.Context``. It skips cleanly
where pypcode or the deity-informant source checkout (:mod:`tuneprog.deity`) is
unavailable. Also puts the repo root on ``sys.path``.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tuneprog import deity

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def ctx6510(tmp_path_factory):
    """Compile+install the 6510 module into a scratch pypcode tree, return its Context."""
    pypcode = pytest.importorskip("pypcode")
    build = deity.sleigh_dir() / "build.py"
    if not build.is_file():
        pytest.skip("no deity-informant source checkout: set DEITY_INFORMANT_SRC")
    procs = tmp_path_factory.mktemp("procs")
    src = Path(pypcode.__file__).parent / "processors"
    langdir = procs / "6510" / "data" / "languages"
    langdir.mkdir(parents=True)
    r = subprocess.run(
        [sys.executable, str(build), "--install", str(langdir)],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        pytest.skip("6510 build failed: " + r.stdout + r.stderr)
    for p in src.iterdir():
        if p.is_dir():
            shutil.copytree(p, procs / p.name, dirs_exist_ok=True)
    pypcode.SPECFILES_DIR = str(procs)
    try:
        return pypcode.Context("6510:LE:16:default")
    except Exception as e:  # pragma: no cover - environment dependent
        pytest.skip("cannot load 6510 context: %r" % e)
