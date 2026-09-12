"""Seed-free floating exploration only; every final threshold needs run.py."""
from __future__ import annotations

import json
import numpy as np

theta = 0.75
a = theta / np.sqrt(2)
c = 2 - theta / 2 - 1 / (np.sqrt(2) * np.tan(a))


def k(x):
    X = np.pi * theta * x
    return (np.sinc((X - a) / np.pi) + np.sinc((X + a) / np.pi)) / (2 * np.sinc(a / np.pi))


rows = []
for radius in [5, 5.5, 6, 6.5, 7, 8, 9, 10, 12]:
    grid = np.linspace(0, radius, 1201)
    best = (float("inf"), 0.0, 0.0)
    for u in grid:
        v = grid[grid + u <= radius]
        e = 2 * (k(u)**2 + k(v)**2 + k(u + v)**2)
        j = int(np.argmin(e))
        if e[j] < best[0]:
            best = (float(e[j]), float(u), float(v[j]))
    epsilon, u, v = best
    rows.append({"radius": radius, "sample_minimum": epsilon, "u": u, "v": v,
                 "sample_gain": epsilon * (c - 2 / radius) / (3 - epsilon)})
print(json.dumps({"status": "exploration only; no lower bound certified", "grid_intervals": 1200,
                  "rows": rows}, indent=2))
