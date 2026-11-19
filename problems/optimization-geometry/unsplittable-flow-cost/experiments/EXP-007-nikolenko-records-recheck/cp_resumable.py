"""A logged, resumable driver for ufclib's cutting-plane frontier evaluator (EXP-007, claim R4, K17 entries).

``ufclib.cutting_plane.frontier_value_cp`` runs the whole search in one call and keeps no record of the levels
it has tested, which a multi-hour run needs. This driver reproduces its binary search over the sorted alpha
levels step for step, calling the library's own ``level_positive`` (separation LP, Bland-rule simplex and the
exact branch-and-bound oracle ``cheapest_routing_below``); it adds only logging, a time limit and a replayable
state file. ufclib is not modified: the oracle is wrapped at run time, in this process, to emit a heartbeat and
to enforce the time limit.

Files (all under the experiment's artifacts folder, ``<id>`` the entry id):

* ``r4-<id>.log``           human log, flushed on every line (header carries the process id);
* ``r4-<id>-levels.json``   the sorted distinct alpha levels and the ceiling (one streaming pass, ~minutes);
* ``r4-<id>-state.jsonl``   one JSON line per tested level: the level index, its outcome and, for a positive
                            level, the full cut set (exact load rows) and witness cost vector. Replaying the
                            file restores (lo, hi, cuts, witness) exactly; a restart repeats at most the one
                            level that was running.
"""

from __future__ import annotations

import json
import os
import time
from fractions import Fraction as F
from pathlib import Path

from ufclib import cutting_plane as cp
from ufclib.decide import alpha_for_routing
from ufclib.enumerate_routings import all_routings, paths_by_terminal, routing_load


class TimeLimit(Exception):
    pass


def _fs(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


class Run:
    def __init__(self, inst, entry_id: str, artifacts: Path, limit_s: float):
        self.inst, self.id, self.art, self.limit_s = inst, entry_id, artifacts, limit_s
        self.log_path = artifacts / f"r4-{entry_id}.log"
        self.levels_path = artifacts / f"r4-{entry_id}-levels.json"
        self.state_path = artifacts / f"r4-{entry_id}-state.jsonl"
        self.t0 = time.time()
        self.oracle_calls = 0

    def say(self, msg: str) -> None:
        line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] +{time.time() - self.t0:9.1f}s {msg}"
        with open(self.log_path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        print(line, flush=True)

    # -- stage 1: the distinct levels, streamed (nothing but the levels is kept) -----------------------
    def levels(self):
        if self.levels_path.exists():
            data = json.loads(self.levels_path.read_text(encoding="utf-8"))
            self.say(f"levels restored from {self.levels_path.name}: {len(data['levels'])} levels")
            return tuple(F(s) for s in data["levels"]), F(data["ceiling"]), data["routings"]
        arcs = list(self.inst.arcs)
        alphas: set[F] = set()
        ceiling, min_cost, n = None, None, 0
        for routing in all_routings(self.inst):
            load = routing_load(self.inst, routing)
            alphas.add(alpha_for_routing(self.inst, load))
            cost = sum((a.cost * load[a.index] for a in arcs), F(0))
            if min_cost is None or cost < min_cost:
                min_cost, ceiling = cost, alpha_for_routing(self.inst, load)
            n += 1
            if n % 16384 == 0:
                self.say(f"level pass: {n} routings, {len(alphas)} distinct levels")
        levels = tuple(sorted(alphas))
        self.levels_path.write_text(json.dumps({"routings": n, "ceiling": _fs(ceiling),
                                                "levels": [_fs(x) for x in levels]}), encoding="utf-8")
        self.say(f"level pass done: {n} routings, {len(levels)} distinct levels, ceiling {_fs(ceiling)}")
        return levels, ceiling, n

    # -- stage 2: replay + binary search -----------------------------------------------------------------
    def replay(self, levels):
        m = len(self.inst.arcs)
        lo, hi = 0, len(levels)
        best_witness = tuple(F(1, m) for _ in range(m))
        lo_cuts: list[list[F]] = []
        tested = []
        spent = 0.0
        if self.state_path.exists():
            for raw in self.state_path.read_text(encoding="utf-8").splitlines():
                if not raw.strip():
                    continue
                rec = json.loads(raw)
                idx = rec["index"]
                if F(rec["level"]) != levels[idx]:
                    raise SystemExit("state file does not match the levels file: refusing to resume")
                tested.append((levels[idx], rec["positive"], rec["solves"], rec["new_cuts"], rec["seconds"]))
                spent += rec["seconds"]
                if rec["positive"]:
                    lo = idx
                    best_witness = tuple(F(s) for s in rec["witness"])
                    lo_cuts = [[F(s) for s in row] for row in rec["cuts"]]
                else:
                    hi = idx
        return lo, hi, best_witness, lo_cuts, tested, spent

    def run(self):
        self.say(f"start pid={os.getpid()} entry={self.id} limit={self.limit_s / 3600:.2f} h")
        levels, ceiling, n_routings = self.levels()
        lo, hi, best_witness, lo_cuts, tested, spent = self.replay(levels)
        if tested:
            self.say(f"resumed: {len(tested)} levels already tested ({spent:.0f} s), lo={lo} hi={hi}")
        per = paths_by_terminal(self.inst)
        original = cp.cheapest_routing_below
        run = self

        def heartbeat(instance, costs, level, _per_terminal=None):
            if time.time() - run.t0 > run.limit_s:
                raise TimeLimit
            run.oracle_calls += 1
            t = time.time()
            out = original(instance, costs, level, _per_terminal)
            run.say(f"  oracle call {run.oracle_calls} at level {_fs(level)} took {time.time() - t:.1f}s "
                    f"({'routing found' if out is not None else 'none below level'})")
            return out

        cp.cheapest_routing_below = heartbeat
        state = "complete"
        try:
            while hi - lo > 1:
                mid = (lo + hi) // 2
                self.say(f"testing level index {mid} of {len(levels)}: {_fs(levels[mid])}  (lo={lo}, hi={hi})")
                t = time.time()
                ok, witness, solves, cuts = cp.level_positive(self.inst, levels[mid], lo_cuts, per)
                dt = time.time() - t
                new_cuts = len(cuts) - len(lo_cuts)
                rec = {"index": mid, "level": _fs(levels[mid]), "positive": ok, "solves": solves,
                       "new_cuts": new_cuts, "seconds": dt}
                if ok:
                    rec["witness"] = [_fs(w) for w in witness]
                    rec["cuts"] = [[_fs(v) for v in row] for row in cuts]
                with open(self.state_path, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(rec) + "\n")
                    fh.flush()
                    os.fsync(fh.fileno())
                tested.append((levels[mid], ok, solves, new_cuts, dt))
                self.say(f"level index {mid} {'POSITIVE' if ok else 'not positive'}: solves={solves} "
                         f"new cuts={new_cuts} in {dt:.1f}s")
                if ok:
                    lo, best_witness, lo_cuts = mid, witness, cuts
                else:
                    hi = mid
        except TimeLimit:
            state = "time limit reached"
            self.say("TIME LIMIT reached; state file holds every completed level")
        finally:
            cp.cheapest_routing_below = original
        out = {
            "state": state,
            "routings": n_routings,
            "levels": len(levels),
            "ceiling": _fs(ceiling),
            "tested": [{"level": _fs(lv), "positive": ok, "solves": s, "new_cuts": c, "seconds": round(sec, 1)}
                       for lv, ok, s, c, sec in tested],
            "lower_bound": _fs(levels[lo]),  # largest level proved positive: frontier value >= this
            "upper_bound": _fs(levels[hi]) if hi < len(levels) else None,  # smallest level proved not positive
            "witness_cost": [_fs(w) for w in best_witness],
            "seconds_this_process": round(time.time() - self.t0, 1),
        }
        if state == "complete":
            out["alpha_max"] = _fs(levels[lo])
        self.say(f"finished: state={state} lower bound {out['lower_bound']} upper bound {out['upper_bound']}")
        return out
