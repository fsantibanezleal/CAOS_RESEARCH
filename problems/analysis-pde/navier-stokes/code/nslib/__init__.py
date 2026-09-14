"""Problem-local library for the navier-stokes research problem.

Modules:
    modulation   the Alpoge-Buckmaster amplitude system and its dissipative extension (numpy)
    cascade      exponent bookkeeping for the layer cascade, with time and hold damping (stdlib)
    boussinesq   GPU pseudo-spectral 2D Boussinesq solver used as the PDE control (torch)
    sweep        batched evaluation of the cascade constraints (torch)

`boussinesq` and `sweep` are imported LAZILY so that `cascade` and `modulation` stay usable
without torch. Repository CI installs numpy and sympy but not torch, and the load-bearing
identities live in the two torch-free modules; an eager import here would have made them
unreachable from the CI lane, which is the whole point of having them under test.

The blowup mechanism these modules describe is due to Diego Cordoba and Luis
Martinez-Zoroa, pushed to smooth forcing by Levent Alpoge and Tristan Buckmaster.
Nothing here is our mechanism.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from . import cascade, cmz_budget, modulation

if TYPE_CHECKING:  # pragma: no cover
    from . import boussinesq, sweep

_LAZY = {"boussinesq", "sweep"}

__all__ = ["boussinesq", "cascade", "cmz_budget", "modulation", "sweep"]


def __getattr__(name: str):
    """Import the torch-backed modules only when they are actually asked for."""
    if name in _LAZY:
        module = importlib.import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
