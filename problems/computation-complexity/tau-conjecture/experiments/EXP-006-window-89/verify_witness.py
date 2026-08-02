"""Adversarial verification of EXP-006 hits: reconstruct an explicit 8-gate
program for each checked hit and verify the 6 roots exactly.

For a hit (state S, extension v, operand b): reconstruct S's 6-gate program
by depth-first search restricted to producing exactly S's values (every
value of a normalized 6-gate program computing the reached set S is a
member of S); then verify v is one op over S's operands, b is an operand,
and f = v*b has the claimed distinct integer roots. Prints the full 8-gate
witness programs.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

from tclib.enum import integer_roots, padd, pmul, psub  # noqa: E402

INPUTS = ((-1,), (1,), (0, 1))


def reconstruct(state_polys):
    target = set(state_polys)

    def dfs(have, prog):
        if not target - set(have):
            return prog
        ops = INPUTS + tuple(have)
        for i, a in enumerate(ops):
            for j, b in enumerate(ops):
                for name, fn in (("+", padd), ("*", pmul), ("-", psub)):
                    if name in ("+", "*") and j < i:
                        continue
                    if name == "-" and i == j:
                        continue
                    val = fn(a, b)
                    if val in target and val not in have:
                        res = dfs(have + [val],
                                  prog + [(a, name, b, val)])
                        if res is not None:
                            return res
        return None

    return dfs([], [])


def main():
    d = json.loads((HERE / "artifacts" / "window.json").read_text("utf-8"))
    hits = d["times_case_hits"][:3]
    for k, h in enumerate(hits):
        state = [tuple(p) for p in h["state"]]
        v, b = tuple(h["v"]), tuple(h["b"])
        prog = reconstruct(state)
        assert prog is not None and len(prog) == 6, "reconstruction failed"
        ops = INPUTS + tuple(state)
        v_ok = None
        for i, a in enumerate(ops):
            for j, c in enumerate(ops):
                for name, fn in (("+", padd), ("*", pmul), ("-", psub)):
                    if name in ("+", "*") and j < i:
                        continue
                    if name == "-" and i == j:
                        continue
                    if fn(a, c) == v:
                        v_ok = (a, name, c)
        assert v_ok is not None, "v is not one op over the state"
        assert b in ops, "b not an operand"
        f = pmul(v, b)
        roots = sorted(integer_roots(f))
        assert roots == h["union_roots"] and len(roots) >= 6
        print(f"WITNESS {k+1}: 8-gate program, roots {roots}")
        for a, name, c, val in prog:
            print(f"   {a} {name} {c} -> {val}")
        print(f"   {v_ok[0]} {v_ok[1]} {v_ok[2]} -> {v}   (gate 7)")
        print(f"   {v} * {b} -> f, roots {roots}   (gate 8)")
        print()
    print("ALL CHECKED WITNESSES VERIFIED (explicit 8-gate programs)")


if __name__ == "__main__":
    main()
