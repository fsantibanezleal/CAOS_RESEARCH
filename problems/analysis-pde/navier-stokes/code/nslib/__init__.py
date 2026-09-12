"""Problem-local library for the navier-stokes research problem.

Modules:
    modulation   the Alpoge-Buckmaster amplitude system and its dissipative extension
    boussinesq   GPU pseudo-spectral 2D Boussinesq solver used as the PDE control
    cascade      exponent bookkeeping for the layer cascade, with time and hold damping

The blowup mechanism these modules describe is due to Diego Cordoba and Luis
Martinez-Zoroa, pushed to smooth forcing by Levent Alpoge and Tristan Buckmaster.
Nothing here is our mechanism.
"""

from . import boussinesq, cascade, modulation

__all__ = ["boussinesq", "cascade", "modulation"]
