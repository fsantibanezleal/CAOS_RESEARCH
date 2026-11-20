"""EXP-007: independent exact re-check of Nikolenko's record instances (hypothesis.md, frozen).

Deterministic, headless, CPU only, exact rationals (no float anywhere), no network.

    .venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/\
EXP-007-nikolenko-records-recheck/run.py --data-root <data root> [--stage R1|R2|R3|R4small|R4k17] [--entry <id>]

Without --stage the four foreground stages R1, R2, R3 and R4small run in order; R4k17 (the two 17-terminal
frontier evaluations, hours) is started separately, one process per entry (--entry), resumable from its logs.
Each stage merges its own section into artifacts/results.json. Exit codes: 0 all claims and instrument checks
hold; 1 a claim R1 to R3 failed or an instrument check failed; 3 data file missing or changed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM_ROOT = HERE.parent.parent
sys.path.insert(0, str(PROBLEM_ROOT / "code"))
sys.path.insert(0, str(HERE))

import family as fam  # noqa: E402
import planarity as pl  # noqa: E402
from ufclib import Instance, InfeasibleFlow  # noqa: E402
from ufclib.decide import alpha_for_routing, decide_instance  # noqa: E402
from ufclib.enumerate_routings import all_routings, paths_by_terminal, routing_load  # noqa: E402
from ufclib.frontier import frontier_value  # noqa: E402
from ufclib.graphs import kuratowski_planarity_by_degrees  # noqa: E402

ARTIFACTS = HERE / "artifacts"
RESULTS = ARTIFACTS / "results.json"
DATA_FILE = "unsplittable-flow-cost/sources/nikolenko-2026/instances.json"
K6_TOPOLOGY = ("unsplittable-flow-cost/sources/nikolenko-2026/repo-certificates-used/"
               "part3_v2_planar_k6_edit_r1_topology_exact_20260810.json")
K17 = ("UF-K17-RECORD", "UF-K17-REFINED")
FAILURES: list[str] = []


def fs(x: F) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def dec(x: F, digits: int = 18) -> str:
    """Decimal expansion of a Fraction by integer arithmetic (truncated), for display only."""
    sign = "-" if x < 0 else ""
    x = abs(x)
    whole, rem = divmod(x.numerator, x.denominator)
    frac = (rem * 10**digits) // x.denominator
    return f"{sign}{whole}.{frac:0{digits}d}"


def say(line: str = "") -> None:
    print(line, flush=True)


def fail(what: str) -> None:
    FAILURES.append(what)
    say(f"  [FAIL] {what}")


# ---------------------------------------------------------------------------------------------------
# Data and results plumbing
# ---------------------------------------------------------------------------------------------------


def load_data(root: Path) -> tuple[list[dict], dict]:
    path = root / DATA_FILE
    if not path.exists():
        say(f"STOP: {path} is missing")
        raise SystemExit(3)
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    sums = path.parent / "SHA256SUMS"
    listed = None
    if sums.exists():
        for line in sums.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1].lstrip("*") == "instances.json":
                listed = parts[0]
    prior = json.loads(RESULTS.read_text(encoding="utf-8")).get("data") if RESULTS.exists() else None
    if prior and prior.get("sha256") != sha:
        say(f"STOP: instances.json SHA-256 {sha} differs from the pinned {prior['sha256']}")
        raise SystemExit(3)
    info = {"file": DATA_FILE, "sha256": sha, "sha256sums_line": listed, "matches_sha256sums": listed == sha,
            "bytes": len(raw)}
    return json.loads(raw.decode("utf-8")), info


def merge_results(updates: dict, per_entry: tuple[str, ...] = ("R1", "R3", "R4", "controls")) -> None:
    """Merge sections into results.json under a lock; per-entry sections merge key by key."""
    ARTIFACTS.mkdir(exist_ok=True)
    lock = ARTIFACTS / ".results.lock"
    deadline = time.time() + 120
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            if time.time() > deadline:
                raise SystemExit("results.json lock held for over 120 s; stop")
            time.sleep(0.2)
    try:
        cur = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {}
        for key, val in updates.items():
            if key in per_entry and isinstance(val, dict) and isinstance(cur.get(key), dict):
                cur[key].update(val)
            else:
                cur[key] = val
        cur["summary"] = summarize(cur)
        cur["environment"] = environment()
        tmp = RESULTS.with_suffix(".tmp")
        tmp.write_text(json.dumps(cur, indent=1, sort_keys=False) + "\n", encoding="utf-8")
        os.replace(tmp, RESULTS)
    finally:
        os.unlink(lock)


def environment() -> dict:
    import networkx

    return {"python": sys.version.split()[0], "networkx": networkx.__version__, "platform": platform.platform(),
            "ufclib": str((PROBLEM_ROOT / "code" / "ufclib").relative_to(PROBLEM_ROOT.parent.parent.parent)),
            "float_policy": "no float: values are strings turned into Fraction; Instance refuses floats"}


def summarize(res: dict) -> dict:
    s: dict = {}
    r1 = res.get("R1", {})
    if r1:
        s["R1"] = {"entries": len(r1), "all_equal": all(v["equal"] and v["paths_match"] for v in r1.values())}
    r2 = res.get("R2")
    if r2:
        s["R2"] = {"all_equal": r2.get("all_equal"), "grid_interval_ok": r2.get("grid", {}).get("interval_ok")}
    r3 = res.get("R3", {})
    if r3:
        s["R3"] = {"entries": len(r3), "certificates_ok": all(v["certificate_ok"] for v in r3.values()),
                   "as_predicted": all(v["agrees_with_hypothesis"] is not False for v in r3.values())}
    r4 = res.get("R4", {})
    if r4:
        s["R4"] = {k: v.get("outcome") for k, v in r4.items()}
    if res.get("controls"):
        s["controls"] = {k: v.get("fired") for k, v in res["controls"].items()}
    return s


# ---------------------------------------------------------------------------------------------------
# Instances
# ---------------------------------------------------------------------------------------------------


def concrete(entries: list[dict]) -> list[dict]:
    return [e for e in entries if isinstance(e.get("arcs"), list) and "x_symbols" not in e]


def by_id(entries: list[dict]) -> dict[str, dict]:
    return {e["id"]: e for e in entries}


def vseq(path) -> tuple[str, ...]:
    return (path[0].tail, *[a.head for a in path])


def alpha_inst_stream(inst: Instance) -> dict:
    """alpha_inst by streaming every routing (no per-routing storage); used where decide_instance would keep
    131,072 load dictionaries, and as a cross-check of decide_instance on the small entries."""
    frac = inst.fractional_cost
    best, cost_good, minimizers, n = None, 0, 0, 0
    for routing in all_routings(inst):
        load = routing_load(inst, routing)
        n += 1
        if inst.cost_of(load) <= frac:
            cost_good += 1
            a = alpha_for_routing(inst, load)
            if best is None or a < best:
                best, minimizers = a, 1
            elif a == best:
                minimizers += 1
    return {"routings": n, "cost_good": cost_good, "alpha_inst": best, "minimizers": minimizers}


def with_costs(inst: Instance, costs) -> Instance:
    arcs = [(a.tail, a.head, a.x, c) for a, c in zip(inst.arcs, costs)]
    return Instance.build(source=inst.source, demands=dict(inst.demands), arcs=arcs, name=inst.name)


# ---------------------------------------------------------------------------------------------------
# R1
# ---------------------------------------------------------------------------------------------------


def expected_paths(entry: dict) -> tuple[str, set | None, int | None]:
    """(source of the expectation, per-terminal path vertex-sequence sets from the JSON or None, count)."""
    if "paths" in entry:
        sets = {t: {tuple([p[0][0]] + [a[1] for a in p]) for p in (v["early"], v["late"])}
                for t, v in entry["paths"].items()}
        return "entry paths list (compared, never used to build)", sets, 2
    counts = entry.get("extractor_check", {}).get("simple_path_counts")
    if counts:
        return "extractor_check.simple_path_counts", None, counts  # type: ignore[return-value]
    return "hypothesis R1: two per terminal on the interval instances", None, 2


def run_r1(entries: list[dict], only: str | None) -> dict:
    out = {}
    say("R1: values with the authors' pricing")
    for e in concrete(entries):
        if only and e["id"] != only:
            continue
        t0 = time.time()
        inst = fam.instance_from_entry(e)
        rec: dict = {"id": e["id"]}
        try:
            inst.check_feasible()
            rec["feasible"] = True
        except InfeasibleFlow as exc:
            rec["feasible"] = False
            rec["feasible_error"] = str(exc)
        per = paths_by_terminal(inst)
        counts = {t: len(p) for t, p in per.items()}
        src, sets, exp = expected_paths(e)
        rec["paths_per_terminal"] = counts
        if isinstance(exp, list):
            want = dict(zip(inst.terminals, exp))
        else:
            want = {t: exp for t in inst.terminals}
        rec["paths_expected_from"] = src
        rec["paths_match"] = counts == want
        if sets is not None:
            rec["paths_equal_json_paths"] = all({vseq(p) for p in per[t]} == sets[t] for t in inst.terminals)
        n_routings = 1
        for c in counts.values():
            n_routings *= c
        claimed = F(e["claimed_value"])
        if n_routings <= 70000:
            rep = decide_instance(inst)
            alpha = rep.alpha_instance
            cost_good = sum(1 for r in rep.routings if r.cost_good)
            minimizers = sum(1 for r in rep.routings if r.cost_good and r.alpha == alpha)
            rec["evaluator"] = "ufclib.decide.decide_instance"
            if n_routings <= 64:
                st = alpha_inst_stream(inst)
                rec["stream_check_equal"] = (st["alpha_inst"], st["cost_good"], st["minimizers"]) == (
                    alpha, cost_good, minimizers)
                if not rec["stream_check_equal"]:
                    fail(f"{e['id']}: streaming evaluator disagrees with decide_instance (instrument check)")
        else:
            st = alpha_inst_stream(inst)
            alpha, cost_good, minimizers = st["alpha_inst"], st["cost_good"], st["minimizers"]
            rec["evaluator"] = ("streaming loop over ufclib.all_routings / routing_load / alpha_for_routing "
                                "(decide_instance would keep 131,072 load dictionaries); the loop is checked "
                                "against decide_instance on every entry of at most 64 routings")
        rec.update(routings=n_routings, cost_good=cost_good, minimizers=minimizers, alpha_inst=fs(alpha),
                   alpha_inst_decimal=dec(alpha), claimed=fs(claimed), equal=alpha == claimed,
                   wall_s=round(time.time() - t0, 2))
        out[e["id"]] = rec
        say(f"  {e['id']}: routings={n_routings} cost_good={cost_good} alpha_inst={fs(alpha)} "
            f"claimed={fs(claimed)} equal={rec['equal']} paths_match={rec['paths_match']} "
            f"minimizers={minimizers} ({rec['wall_s']} s)")
        if not rec["feasible"]:
            fail(f"{e['id']}: x is not a feasible fractional flow: {rec['feasible_error']}")
        if not rec["equal"]:
            fail(f"{e['id']}: alpha_inst {fs(alpha)} != claimed {fs(claimed)}")
        if not rec["paths_match"]:
            fail(f"{e['id']}: path counts {counts} differ from the transcription {want}")
        if rec.get("paths_equal_json_paths") is False:
            fail(f"{e['id']}: enumerated paths differ from the JSON paths list")
    merge_results({"R1": out})
    return out


# ---------------------------------------------------------------------------------------------------
# Controls (a) and (b)
# ---------------------------------------------------------------------------------------------------


def control_a(entries: list[dict], entry_id: str, terminal: str, delta: F) -> dict:
    """One demand changed by one unit in its last printed digit, with the flow kept feasible: the extra
    ``delta`` of that terminal rides on one of its two paths (both variants are run and reported)."""
    e = by_id(entries)[entry_id]
    base = fam.instance_from_entry(e)
    per = paths_by_terminal(base)
    paths = per[terminal]
    paid = next(p for p in paths if p[-1].cost > 0)
    free = next(p for p in paths if p[-1].cost == 0)
    rec = {"entry": entry_id, "terminal": terminal, "delta": fs(delta), "variants": {}}
    for label, path in (("on the early (paid) path", paid), ("on the late (free) path", free)):
        on = {a.index for a in path}
        arcs = [(a.tail, a.head, a.x + (delta if a.index in on else 0), a.cost) for a in base.arcs]
        demands = dict(base.demands)
        demands[terminal] += delta
        mod = Instance.build(source=base.source, demands=demands, arcs=arcs, name=f"{entry_id}+delta")
        mod.check_feasible()
        t0 = time.time()
        st = alpha_inst_stream(mod)
        rec["variants"][label] = {"alpha_inst": fs(st["alpha_inst"]), "equals_claim": st["alpha_inst"] == F(e["claimed_value"]),
                                  "difference_from_claim": fs(st["alpha_inst"] - F(e["claimed_value"])),
                                  "wall_s": round(time.time() - t0, 1)}
        say(f"  control a {entry_id} {terminal} +{fs(delta)} {label}: alpha_inst={fs(st['alpha_inst'])} "
            f"equals claim={st['alpha_inst'] == F(e['claimed_value'])}")
    rec["fired"] = any(not v["equals_claim"] for v in rec["variants"].values())
    return rec


def control_b(entries: list[dict], entry_id: str) -> dict:
    e = by_id(entries)[entry_id]
    base = fam.instance_from_entry(e)
    zero = with_costs(base, [F(0)] * len(base.arcs))
    rep = decide_instance(zero)
    # every routing costs 0 <= 0, so alpha_inst is the minimum of alpha over all routings; the all-early
    # routing is the one using each terminal's paid path
    per = paths_by_terminal(zero)
    early = tuple(next(p for p in per[t] if base.arcs[p[-1].index].cost > 0) for t in zero.terminals)
    all_early = alpha_for_routing(zero, routing_load(zero, early))
    alphas = sorted({r.alpha for r in rep.routings})
    claim = F(e["claimed_value"])
    rec = {"entry": entry_id, "alpha_inst_zero_costs": fs(rep.alpha_instance), "all_early_alpha": fs(all_early),
           "min_over_all_routings": fs(alphas[0]), "claim": fs(claim),
           "cost_good_routings": sum(1 for r in rep.routings if r.cost_good), "routings": len(rep.routings),
           "fired": rep.alpha_instance != claim and rep.alpha_instance in (F(0), all_early, alphas[0])}
    say(f"  control b {entry_id}: zero costs -> alpha_inst={fs(rep.alpha_instance)} (all-early {fs(all_early)}, "
        f"claim {fs(claim)}) fired={rec['fired']}")
    return rec


def run_controls_ab(entries: list[dict], big: bool) -> dict:
    out = {}
    say("Controls (a) and (b)")
    ids = by_id(entries)
    # (a) the K17 entry: terminal t1, last printed digit of d (10^-9 for the record; its refinement prints 10^-15)
    out["a_demand_plus_one_unit"] = control_a(entries, "UF-K17-RECORD", "t1", F(1, 10**9)) if big else {
        "fired": None, "note": "not run in this invocation (--no-big)"}
    out["b_costs_zeroed"] = {}
    for eid in ("UF-4INT-n1000", "UF-PLANAR-K6"):
        if eid in ids:
            out["b_costs_zeroed"][eid] = control_b(entries, eid)
    out["b_costs_zeroed"]["fired"] = all(v["fired"] for k, v in out["b_costs_zeroed"].items() if k != "fired")
    if big:
        out["b_costs_zeroed"]["UF-K17-RECORD"] = None  # filled below
        rec = control_b_big(entries, "UF-K17-RECORD")
        out["b_costs_zeroed"]["UF-K17-RECORD"] = rec
        out["b_costs_zeroed"]["fired"] = all(v["fired"] for k, v in out["b_costs_zeroed"].items() if k != "fired")
    out["b_costs_zeroed"]["fired"] = bool(out["b_costs_zeroed"]["fired"])
    return out


def control_b_big(entries: list[dict], entry_id: str) -> dict:
    """Control (b) on a large entry without storing the routings: zero costs make every routing cost-good, so
    alpha_inst is the least alpha over all routings."""
    e = by_id(entries)[entry_id]
    base = fam.instance_from_entry(e)
    zero = with_costs(base, [F(0)] * len(base.arcs))
    st = alpha_inst_stream(zero)
    per = paths_by_terminal(zero)
    early = tuple(next(p for p in per[t] if base.arcs[p[-1].index].cost > 0) for t in zero.terminals)
    all_early = alpha_for_routing(zero, routing_load(zero, early))
    claim = F(e["claimed_value"])
    rec = {"entry": entry_id, "alpha_inst_zero_costs": fs(st["alpha_inst"]), "all_early_alpha": fs(all_early),
           "claim": fs(claim), "cost_good_routings": st["cost_good"], "routings": st["routings"],
           "fired": st["alpha_inst"] != claim}
    say(f"  control b {entry_id}: zero costs -> alpha_inst={fs(st['alpha_inst'])} (all-early {fs(all_early)}, "
        f"claim {fs(claim)}) fired={rec['fired']}")
    return rec


# ---------------------------------------------------------------------------------------------------
# R2
# ---------------------------------------------------------------------------------------------------


def run_r2(entries: list[dict]) -> dict:
    say("R2: families")
    ids = by_id(entries)
    fam4 = ids["UF-4INT-FAMILY"]
    out: dict = {"builder_validation": {}, "n_series": [], "grid": {}, "ternary": []}

    # builder validation first: the symbolic four-interval member and the ternary builder must reproduce the
    # concrete entries exactly
    for n, eid in ((67, "UF-4INT-n67"), (68, "UF-4INT-n68"), (1000, "UF-4INT-n1000")):
        rep = fam.reproduces_entry(fam.four_interval_member(fam4, F(3, 20), F(1, n)), ids[eid])
        out["builder_validation"][eid] = rep
        say(f"  builder reproduces {eid}: {rep['ok']} (flow scale {rep.get('flow_scale')}, cost scale {rep.get('cost_scale')})")
        if not rep["ok"]:
            fail(f"four-interval builder does not reproduce {eid}: {rep['reason']}")
    rep = fam.reproduces_entry(fam.ternary_member(F(1, 10)), ids["UF-E3-TERNARY-eta1over10"])
    out["builder_validation"]["UF-E3-TERNARY-eta1over10"] = rep
    say(f"  builder reproduces UF-E3-TERNARY-eta1over10: {rep['ok']}")
    if not rep["ok"]:
        fail(f"ternary builder does not reproduce the concrete entry: {rep['reason']}")
    if FAILURES:
        merge_results({"R2": {**out, "all_equal": False, "aborted": "builder validation failed"}})
        return out

    all_equal = True
    for n in (67, 68, 100, 1000, 10**4, 10**6):
        t0 = time.time()
        inst = fam.four_interval_member(fam4, F(3, 20), F(1, n))
        alpha = decide_instance(inst).alpha_instance
        want = F(182359, 160000) - F(1, n)
        ok = alpha == want
        all_equal &= ok
        out["n_series"].append({"n": n, "alpha_inst": fs(alpha), "expected": fs(want), "equal": ok,
                                "below_9_over_8": alpha < F(9, 8), "wall_s": round(time.time() - t0, 2)})
        say(f"  n={n}: alpha_inst={fs(alpha)} expected={fs(want)} equal={ok} (below 9/8: {alpha < F(9, 8)})")
        if not ok:
            fail(f"four-interval n={n}: alpha_inst {fs(alpha)} != {fs(want)}")

    eps = F(1, 10**6)
    rows = []
    for k in range(40, 81):
        t = F(k, 400)
        inst = fam.four_interval_member(fam4, t, eps)
        alpha = decide_instance(inst).alpha_instance
        closed = fam.four_interval_closed_form(t, eps)
        rows.append({"k": k, "t": fs(t), "alpha_inst": fs(alpha), "closed_form": fs(closed), "equal": alpha == closed,
                     "eps_below_C_minus_1": eps < closed + eps - 1})
        if alpha != closed:
            fail(f"grid k={k}: alpha_inst {fs(alpha)} != closed form {fs(closed)}")
    best = max(F(r["alpha_inst"]) for r in rows)
    argmax = [r["k"] for r in rows if F(r["alpha_inst"]) == best]
    lo41, hi41 = fam.sqrt41_bounds()
    # C* = (299 - 41 sqrt41)/32 is decreasing in sqrt41: lo41 < sqrt41 < hi41 brackets it
    c_star_low = (299 - 41 * hi41) / 32
    c_star_high = (299 - 41 * lo41) / 32
    below_c_star = best < c_star_low  # best < C*_low <= C*
    above = best > c_star_high - F(1, 10**4)  # best > C*_high - 1e-4 >= C* - 1e-4
    grid = {"eps": fs(eps), "points": len(rows), "all_equal_closed_form": all(r["equal"] for r in rows),
            "max_alpha_inst": fs(best), "max_alpha_inst_decimal": dec(best), "argmax_k": argmax,
            "argmax_t": [fs(F(k, 400)) for k in argmax], "argmax_in_{59,60}": set(argmax) <= {59, 60},
            "sqrt41_lower": fs(lo41), "sqrt41_upper": fs(hi41),
            "sqrt41_bounds_verified_by_squaring": bool(lo41 * lo41 < 41 < hi41 * hi41),
            "c_star_lower_bound": fs(c_star_low), "c_star_upper_bound": fs(c_star_high),
            "c_star_lower_bound_decimal": dec(c_star_low), "c_star_upper_bound_decimal": dec(c_star_high),
            "max_below_c_star": bool(below_c_star), "max_above_c_star_minus_1e-4": bool(above),
            "gap_c_star_minus_max_lower": fs(c_star_low - best), "gap_c_star_minus_max_upper": fs(c_star_high - best),
            "rows": rows}
    grid["interval_ok"] = bool(below_c_star and above)
    out["grid"] = grid
    say(f"  grid: max alpha_inst={dec(best)} at k={argmax}; C* in ({dec(c_star_low)}, {dec(c_star_high)}); "
        f"below C*={below_c_star}; above C*-1e-4={above}; argmax in {{59,60}}={grid['argmax_in_{59,60}']}")
    if not grid["interval_ok"]:
        fail("grid maximum is not inside the interval (C* - 1e-4, C*)")
    if not grid["argmax_in_{59,60}"]:
        fail(f"grid maximum attained at k={argmax}, not at 59 or 60 (hypothesis R2)")
    all_equal &= grid["all_equal_closed_form"] and grid["interval_ok"] and grid["argmax_in_{59,60}"]

    for eta in (F(1, 2), F(1, 10), F(1, 100), F(1, 1000)):
        inst = fam.ternary_member(eta)
        alpha = decide_instance(inst).alpha_instance
        want = fam.ternary_closed_form(eta)
        ok = alpha == want and alpha < F(9, 8)
        all_equal &= ok
        out["ternary"].append({"eta": fs(eta), "alpha_inst": fs(alpha), "expected": fs(want), "equal": alpha == want,
                               "below_9_over_8": alpha < F(9, 8)})
        say(f"  ternary eta={fs(eta)}: alpha_inst={fs(alpha)} expected (3-eta)^2/8={fs(want)} equal={alpha == want} "
            f"below 9/8={alpha < F(9, 8)}")
        if not ok:
            fail(f"ternary eta={fs(eta)}: alpha_inst {fs(alpha)} vs {fs(want)}")
    out["all_equal"] = bool(all_equal)
    merge_results({"R2": out})
    return out


# ---------------------------------------------------------------------------------------------------
# R3
# ---------------------------------------------------------------------------------------------------

EXPECTED_PLANAR = {"UF-K17-RECORD": False, "UF-K17-REFINED": False, "UF-4INT-n67": True, "UF-4INT-n68": True,
                   "UF-4INT-n1000": True, "UF-4INT-8867": True, "UF-PLANAR-K6": True, "UF-7VERTEX-16over15": True}


def _canon_cycle(face) -> tuple:
    face = list(face)
    i = min(range(len(face)), key=lambda j: face[j])
    return tuple(face[i:] + face[:i])


def run_r3(entries: list[dict], root: Path) -> dict:
    say("R3: planarity")
    out = {}
    insts = {}
    for e in concrete(entries):
        inst = fam.instance_from_entry(e)
        insts[e["id"]] = inst
        t0 = time.time()
        edges = [(a.tail, a.head) for a in inst.arcs]
        simple = {frozenset(x) for x in edges if x[0] != x[1]}
        deg = kuratowski_planarity_by_degrees(inst)
        sol = pl.decide_planarity(list(inst.vertices), edges)
        rec = {"id": e["id"], "vertices": len(inst.vertices), "arcs": len(inst.arcs), "simple_edges": len(simple),
               "degree_test": deg, "solver_planar": sol["planar"], "certificate": sol["certificate"],
               "certificate_ok": sol["certificate_ok"], "wall_s": round(time.time() - t0, 2)}
        if sol["planar"]:
            rec.update(V=sol["V"], E=sol["E"], F=sol["F"], components=sol["components"],
                       euler=sol["V"] - sol["E"] + sol["F"])
        else:
            rec.update(kuratowski_type=sol["kuratowski_type"], kuratowski_edges=len(sol["kuratowski_edges"]),
                       suppressed_vertices=sol["suppressed_vertices"],
                       kuratowski_subgraph=sol["kuratowski_edges"])
        want = EXPECTED_PLANAR.get(e["id"])
        rec["hypothesis_expectation"] = ("planar" if want else "non-planar") if want is not None else "none (not stated)"
        rec["agrees_with_hypothesis"] = None if want is None else (sol["planar"] == want)
        rec["degree_test_consistent"] = deg is None or (deg is True and sol["planar"])
        out[e["id"]] = rec
        say(f"  {e['id']}: degree test={deg} solver planar={sol['planar']} cert ok={sol['certificate_ok']} "
            + (f"V={rec['V']} E={rec['E']} F={rec['F']}" if sol["planar"]
               else f"{rec['kuratowski_type']} subdivision, {rec['kuratowski_edges']} edges"))
        if not sol["certificate_ok"]:
            fail(f"{e['id']}: planarity certificate rejected by the checker")
        if rec["agrees_with_hypothesis"] is False:
            fail(f"{e['id']}: solver says {'planar' if sol['planar'] else 'non-planar'}, hypothesis expects {rec['hypothesis_expectation']}")
        if not rec["degree_test_consistent"]:
            fail(f"{e['id']}: degree test and solver disagree")

    # repository topology certificate for UF-PLANAR-K6
    k6 = {}
    cert_path = root / K6_TOPOLOGY
    if cert_path.exists() and "UF-PLANAR-K6" in insts:
        cert = json.loads(cert_path.read_text(encoding="utf-8"))
        inst = insts["UF-PLANAR-K6"]
        inst_edges = {frozenset((a.tail, a.head)) for a in inst.arcs}
        cert_edges = {frozenset(x) for x in cert["raw_directed_arcs"] if x[0] != x[1]}
        rot = {v: list(ws) for v, ws in cert["rotation"].items()}
        cert_vertices = sorted(rot)
        check = pl.check_planar_certificate(cert_vertices, [tuple(e) for e in cert_edges], rot)
        faces = pl.trace_faces(rot)
        stored = sorted(_canon_cycle(f) for f in cert["faces"])
        traced = sorted(_canon_cycle([d[0] for d in f]) for f in faces)
        extra = sorted(sorted(e) for e in cert_edges - inst_edges)
        missing = sorted(sorted(e) for e in inst_edges - cert_edges)
        # the pendant edges of the certificate that the instance lacks: drop them from graph and rotation
        reduced = {v: [w for w in ws if frozenset((v, w)) in inst_edges] for v, ws in rot.items()
                   if any(v in e for e in inst_edges)}
        reduced_check = pl.check_planar_certificate(
            sorted(reduced), [tuple(e) for e in inst_edges], reduced)
        k6 = {"certificate_file": K6_TOPOLOGY.split("/")[-1],
              "certificate_edge_set_equals_instance_edge_set": cert_edges == inst_edges,
              "certificate_edges_not_in_instance": extra, "instance_edges_not_in_certificate": missing,
              "certificate_as_stored": {"V": check["V"], "E": check["E"], "F": check["F"], "ok": check["ok"],
                                        "euler": check["V"] - check["E"] + (check["F"] or 0),
                                        "stored_counts": [cert["vertices"], cert["edges"], cert["faces_count"]],
                                        "traced_faces_equal_stored_faces": stored == traced},
              "restricted_to_instance_edge_set": {"V": reduced_check["V"], "E": reduced_check["E"],
                                                  "F": reduced_check["F"], "ok": reduced_check["ok"],
                                                  "euler": reduced_check["V"] - reduced_check["E"] + (reduced_check["F"] or 0)},
              "predicted_16_21_7": (check["V"], check["E"], check["F"]) == (16, 21, 7)}
        say(f"  K6 topology certificate: edge set equal to instance's: {cert_edges == inst_edges}; "
            f"extra edges in certificate {extra}; as stored V={check['V']} E={check['E']} F={check['F']} ok={check['ok']}; "
            f"restricted to the instance V={reduced_check['V']} E={reduced_check['E']} F={reduced_check['F']} ok={reduced_check['ok']}")
        if not check["ok"] or not reduced_check["ok"]:
            fail("UF-PLANAR-K6: the repository rotation system is not genus 0 by face tracing")
        if not k6["predicted_16_21_7"]:
            fail("UF-PLANAR-K6: face tracing does not give 16 vertices, 21 edges, 7 faces")
        if not k6["certificate_as_stored"]["traced_faces_equal_stored_faces"]:
            fail("UF-PLANAR-K6: traced faces differ from the stored faces")
    else:
        k6 = {"not_evaluated": f"{K6_TOPOLOGY} not found under the data root"}
        fail("K6 topology certificate not found")

    # control (c): the checker rejects a certificate of another graph
    ctrl = {"fired": None}
    if cert_path.exists():
        rot = {v: list(ws) for v, ws in json.loads(cert_path.read_text(encoding="utf-8"))["rotation"].items()}
        tests = {}
        for other in ("UF-4INT-n67", "UF-7VERTEX-16over15", "UF-E3-TERNARY-eta1over10"):
            inst = insts[other]
            r = pl.check_planar_certificate(list(inst.vertices), [(a.tail, a.head) for a in inst.arcs], rot)
            tests[f"K6 rotation system offered for {other}"] = {"accepted": r["ok"], "reason": r["reason"]}
        sub_k17 = out["UF-K17-RECORD"]["kuratowski_subgraph"]
        for other in ("UF-PLANAR-K6", "UF-4INT-n67"):
            inst = insts[other]
            r = pl.check_kuratowski_certificate(list(inst.vertices), [(a.tail, a.head) for a in inst.arcs],
                                                [tuple(x) for x in sub_k17])
            tests[f"K17-RECORD Kuratowski subgraph offered for {other}"] = {"accepted": r["ok"], "reason": r["reason"]}
        # not a control: the two K17 graphs share their edges up to the endpoints that differ, so the
        # record's subgraph may also be a subgraph of the refinement; stated as a fact, whatever the answer
        inst = insts["UF-K17-REFINED"]
        r = pl.check_kuratowski_certificate(list(inst.vertices), [(a.tail, a.head) for a in inst.arcs],
                                            [tuple(x) for x in sub_k17])
        cross = {"K17-RECORD Kuratowski subgraph offered for UF-K17-REFINED": {"accepted": r["ok"], "reason": r["reason"]}}
        # same vertex set, one edge replaced: the K6 graph with (v0,t0) moved to (v0,t5)
        k6e = [tuple(sorted(e)) for e in {frozenset(x) for x in json.loads(cert_path.read_text(encoding="utf-8"))["raw_directed_arcs"]}]
        k6e = [e for e in k6e if e != ("t0", "v0")] + [("t5", "v0")]
        r = pl.check_planar_certificate(sorted(rot), k6e, rot)
        tests["K6 rotation system offered for the K6 graph with one edge replaced (same vertices)"] = {
            "accepted": r["ok"], "reason": r["reason"]}
        # a genuine certificate tampered: swap two neighbours in the K6 rotation at v3 (degree 4)
        bad = {v: list(ws) for v, ws in rot.items()}
        bad["v3"][1], bad["v3"][2] = bad["v3"][2], bad["v3"][1]
        r = pl.check_planar_certificate(sorted(bad), [tuple(e) for e in {frozenset(x) for x in json.loads(cert_path.read_text(encoding='utf-8'))['raw_directed_arcs']}], bad)
        tests["K6 rotation with two neighbours swapped at v3"] = {"accepted": r["ok"], "reason": r["reason"]}
        ctrl = {"tests": tests, "fired": all(not v["accepted"] for v in tests.values()),
                "cross_validity_not_a_control": cross}
        say(f"  control c: every foreign or tampered certificate rejected: {ctrl['fired']}")
        for k, v in tests.items():
            say(f"    {k}: accepted={v['accepted']} ({v['reason']})")
    if not ctrl["fired"]:
        fail("control (c): the planarity checker accepted a certificate of another graph")
    out_meta = {"UF-PLANAR-K6": {**out["UF-PLANAR-K6"], "repository_topology_certificate": k6}}
    out.update(out_meta)
    merge_results({"R3": out, "controls": {"c_foreign_certificate": ctrl}})
    return out


# ---------------------------------------------------------------------------------------------------
# R4
# ---------------------------------------------------------------------------------------------------


def outcome(alpha_max: F, claim: F) -> str:
    if alpha_max == claim:
        return "equals claim"
    return "exceeds claim" if alpha_max > claim else "BELOW claim (instrument check failed)"


def run_r4_small(entries: list[dict], only: str | None) -> dict:
    say("R4small: frontier value, entries with at most 64 routings")
    out = {}
    for e in concrete(entries):
        if e["id"] in K17 or (only and e["id"] != only):
            continue
        inst = fam.instance_from_entry(e)
        n = 1
        for p in paths_by_terminal(inst).values():
            n *= len(p)
        if n > 64:
            continue
        t0 = time.time()
        res = frontier_value(inst)
        wall = time.time() - t0
        claim = F(e["claimed_value"])
        # independent re-check of the witness: the instance priced with the witness vector, decided by the
        # plain enumeration (every cost-good routing, its least violation)
        wit = list(res.witness_cost)
        chk = decide_instance(with_costs(inst, wit))
        rec = {"id": e["id"], "routings": n, "evaluator": "ufclib.frontier.frontier_value", "alpha_max": fs(res.alpha_max),
               "alpha_max_decimal": dec(res.alpha_max), "claimed": fs(claim), "outcome": outcome(res.alpha_max, claim),
               "excess_over_claim": fs(res.alpha_max - claim), "ceiling": fs(res.ceiling),
               "witness_cost_vector": [fs(c) for c in wit], "witness_arcs": [f"{a.tail}->{a.head}" for a in inst.arcs],
               "witness_recheck_alpha_inst": fs(chk.alpha_instance),
               "witness_recheck_equals_alpha_max": chk.alpha_instance == res.alpha_max, "wall_s": round(wall, 2)}
        out[e["id"]] = rec
        say(f"  {e['id']}: alpha_max={fs(res.alpha_max)} claim={fs(claim)} -> {rec['outcome']} "
            f"(excess {fs(res.alpha_max - claim)}); witness recheck equal={rec['witness_recheck_equals_alpha_max']} "
            f"({rec['wall_s']} s)")
        if res.alpha_max < claim:
            fail(f"{e['id']}: frontier value below the claim: instrument check failed")
        if not rec["witness_recheck_equals_alpha_max"]:
            fail(f"{e['id']}: witness cost vector does not reproduce alpha_max by plain enumeration")
    merge_results({"R4": out})
    return out


def run_r4_k17(entries: list[dict], entry_id: str, limit_hours: float) -> dict:
    import cp_resumable

    e = by_id(entries)[entry_id]
    inst = fam.instance_from_entry(e)
    ARTIFACTS.mkdir(exist_ok=True)
    run = cp_resumable.Run(inst, entry_id, ARTIFACTS, limit_hours * 3600)
    res = run.run()
    claim = F(e["claimed_value"])
    rec = {"id": entry_id, "evaluator": "ufclib.cutting_plane.level_positive via cp_resumable.Run (the binary search "
           "of frontier_value_cp, logged and resumable)", "claimed": fs(claim), **res}
    if res["state"] == "complete":
        am = F(res["alpha_max"])
        rec["outcome"] = outcome(am, claim)
        rec["excess_over_claim"] = fs(am - claim)
        wit = [F(s) for s in res["witness_cost"]]
        run.say("witness re-check by plain enumeration (priced with the witness vector) ...")
        st = alpha_inst_stream(with_costs(inst, wit))
        rec["witness_recheck_alpha_inst"] = fs(st["alpha_inst"])
        rec["witness_recheck_equals_alpha_max"] = st["alpha_inst"] == am
        run.say(f"witness re-check: alpha_inst under the witness = {fs(st['alpha_inst'])}, equals alpha_max: "
                f"{st['alpha_inst'] == am}")
        if am < claim:
            fail(f"{entry_id}: frontier value below the claim: instrument check failed")
        if st["alpha_inst"] != am:
            fail(f"{entry_id}: witness does not reproduce alpha_max by plain enumeration")
    else:
        lo, hi = F(res["lower_bound"]), res["upper_bound"]
        rec["outcome"] = (f"interval at the limit: frontier value >= {res['lower_bound']}"
                          + (f" and < {hi}" if hi else "") + f" (claim {fs(claim)}; lower bound "
                          f"{'above' if lo > claim else 'not above'} the claim)")
    merge_results({"R4": {entry_id: rec}})
    return rec


# ---------------------------------------------------------------------------------------------------


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-root", default=os.environ.get("CAOS_RESEARCH_DATA"),
                    help="data root holding unsplittable-flow-cost/sources/nikolenko-2026 (or CAOS_RESEARCH_DATA)")
    ap.add_argument("--stage", choices=["R1", "R2", "R3", "R4small", "R4k17"], default=None)
    ap.add_argument("--entry", default=None, help="restrict R1/R4small to one entry; required for R4k17")
    ap.add_argument("--limit-hours", type=float, default=6.0, help="R4k17 time limit per process")
    ap.add_argument("--no-big", action="store_true", help="skip the K17-sized controls (a) and (b)")
    args = ap.parse_args(argv)
    if not args.data_root:
        say("STOP: give --data-root or set CAOS_RESEARCH_DATA")
        return 3
    root = Path(args.data_root)
    ARTIFACTS.mkdir(exist_ok=True)
    entries, info = load_data(root)
    merge_results({"data": info})
    say(f"data: {info['file']} sha256={info['sha256']} (matches SHA256SUMS: {info['matches_sha256sums']})")
    stages = [args.stage] if args.stage else ["R1", "R2", "R3", "R4small"]
    t0 = time.time()
    for st in stages:
        if st == "R1":
            run_r1(entries, args.entry)
            if not args.entry:
                ctrls = run_controls_ab(entries, big=not args.no_big)
                merge_results({"controls": ctrls})
                if ctrls["a_demand_plus_one_unit"].get("fired") is False:
                    fail("control (a): the perturbed K17 instance still gives the claimed value")
                if not ctrls["b_costs_zeroed"]["fired"]:
                    fail("control (b): zeroed costs still give the claimed value")
        elif st == "R2":
            run_r2(entries)
        elif st == "R3":
            run_r3(entries, root)
        elif st == "R4small":
            run_r4_small(entries, args.entry)
        elif st == "R4k17":
            if args.entry not in K17:
                say(f"STOP: --entry must be one of {K17} for R4k17")
                return 3
            run_r4_k17(entries, args.entry, args.limit_hours)
    say(f"stages {stages} done in {time.time() - t0:.1f} s; failures: {len(FAILURES)}")
    for f in FAILURES:
        say(f"  FAILED: {f}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
