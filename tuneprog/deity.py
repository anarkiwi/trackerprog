"""The deity-informant source tree: the ``ghidra/6510`` SLEIGH build and the
``examples`` demo ship only in a source checkout, never in the wheel.

``$DEITY_INFORMANT_SRC`` names the checkout; otherwise it is the tree an
editable install of ``deity_informant`` points into.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import deity_informant


def src():
    """The deity-informant checkout root."""
    env = os.environ.get("DEITY_INFORMANT_SRC")
    return Path(env) if env else Path(deity_informant.__file__).resolve().parents[1]


def sleigh_dir():
    """``ghidra/6510`` of the checkout: ``build.py`` and ``smc.py``."""
    return src() / "ghidra" / "6510"


def on_path():
    """Make ``examples.hello_world``, ``build`` and ``smc`` importable; returns :func:`src`."""
    root = src()
    for p in (str(root), str(sleigh_dir())):
        if p not in sys.path:
            sys.path.insert(0, p)
    return root
