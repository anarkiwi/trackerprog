"""Shared fixtures for the tuneprog/trackerprog test suite.

``ctx6510`` compiles+installs deity-informant's 6510 SLEIGH module into a scratch
pypcode processors tree and returns a loaded ``pypcode.Context``; it skips cleanly
where pypcode or the SLEIGH build is unavailable. Also puts the repo root on
``sys.path``.
"""

import sys
from pathlib import Path

import pytest

from deity_informant.sleigh import pypcode_context

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def ctx6510(tmp_path_factory):
    """Compile+install the 6510 module into a scratch pypcode tree, return its Context."""
    pytest.importorskip("pypcode")
    try:
        return pypcode_context(tmp_path_factory.mktemp("procs"))
    except SystemExit as e:  # pragma: no cover - environment dependent
        pytest.skip("6510 build failed: %s" % e)
