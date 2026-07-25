"""ufclib: exact decision machinery for single-source unsplittable flow with costs.

The programme's ground truth (plan.md, rung UF-P0). Everything is exact: arc data,
demands and every reported quantity are ``fractions.Fraction``. Floats are banned in this
problem (methodology/04 and the problem's standing policy), because every quantity that
arises is a rational of modest size and there is therefore no exploration regime that
would justify them.

Written from the conjecture statement as transcribed in
``context/2026-07-24-literature-status-dossier.md``. It does not import, execute or
consult any third-party verifier; see the independence rule in
``context/2026-07-24-claimed-counterexample-dossier.md``.
"""

from .instance import Arc, Instance, InfeasibleFlow
from .enumerate_routings import simple_paths, all_routings, routing_load
from .decide import (
    RoutingReport,
    InstanceReport,
    congestion_violations,
    decide_instance,
    alpha_for_routing,
)
from .graphs import is_acyclic, has_k4_subdivision, kuratowski_planarity_by_degrees

__all__ = [
    "Arc",
    "Instance",
    "InfeasibleFlow",
    "simple_paths",
    "all_routings",
    "routing_load",
    "RoutingReport",
    "InstanceReport",
    "congestion_violations",
    "decide_instance",
    "alpha_for_routing",
    "is_acyclic",
    "has_k4_subdivision",
    "kuratowski_planarity_by_degrees",
]
