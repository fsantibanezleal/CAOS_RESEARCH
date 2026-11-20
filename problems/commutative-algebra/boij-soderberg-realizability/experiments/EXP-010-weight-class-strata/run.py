"""EXP-010: pure pairs in the weight-class strata S(m; i, j), e = 6 and 7 in the five open characteristics (and e = 8, exploratory).

Run from the repository root, with the repository virtual environment:
    python <this file> gates                          G1 (a) to (d) and G3 (pytest's exit code); exit 1 on a failure
    python <this file> cases --family C|Q|E [--only e,p[+e,p]] [--workers N] [--budget-seconds N] [--chunk N]
                                                      resumable (results are stored per stratum); the early stop of a stratum is at 5 pure
                                                      members; family C is followed by G4 and the control part of G1; Q and E need both
    python <this file> second [--workers N] [--out-dir D]
                                                      G2: Singular 4.3.2 (Plural, through WSL) on the first two pure members of each stratum
                                                      that has one (at most ten per pair); the scripts are copied to artifacts/singular
    python <this file> table                          totals, predictions P1 to P5 into results.json, then results-summary.md; prints the
                                                      table of the pairs

The hypothesis is hypothesis.md (frozen).  First instrument: exp010_routine.py over `uhlib`.  Second instrument: Singular through
EXP-009's generator (exp009_singular.py).  At most 16 worker processes and five hours of wall time in total (`cases` stops handing out
work at the budget).  No machine path is written to any artifact.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from collections import deque
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, ThreadPoolExecutor, wait
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE))
SIBLING = HERE.parent / "EXP-009-linear-family-below-2e"
if str(SIBLING) not in sys.path:
    sys.path.append(str(SIBLING))  # appended: EXP-009 has its own run.py and make_summary.py, which must not shadow this folder's

import exp010_routine as X  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
RESULTS = ART / "results.json"
T0 = time.time()
MAX_WORKERS = 16
BUDGET_SECONDS = 5 * 3600
SAVE_EVERY = 30.0
MAX_ACTIVE = 24
G2_PER_STRATUM = 2
G2_PER_PAIR = 10
make_spec = X.make_spec


def log(msg):
    print("[%8.1fs] %s" % (time.time() - T0, msg), flush=True)


def load():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    return {"experiment": "EXP-010", "hypothesis": "hypothesis.md (frozen)", "strata": {}, "gates": {}, "runs": [],
            "budget": {"used_seconds": 0.0, "limit_seconds": BUDGET_SECONDS}}


def save(res):
    ART.mkdir(exist_ok=True)
    tmp = RESULTS.with_suffix(".tmp")
    tmp.write_text(json.dumps(res, separators=(",", ":")), encoding="utf-8", newline="\n")
    tmp.replace(RESULTS)


def opt(name, default):
    for a in sys.argv[2:]:
        if a.startswith("--%s=" % name):
            return a.split("=", 1)[1]
    for k, a in enumerate(sys.argv[2:-1], start=2):
        if a == "--%s" % name:
            return sys.argv[k + 1]
    return default


def workers():
    return max(1, min(MAX_WORKERS, int(opt("workers", MAX_WORKERS))))


def pair_list():
    only = opt("only", "")
    if not only:
        return None
    return {tuple(int(t) for t in item.split(",")) for item in only.replace(";", "+").split("+")}


# ------------------------------------------------------------------ the scheduler
class Stratum:
    """The state of a stratum while its chunks and Betti tables are in flight."""

    def __init__(self, spec, chunk):
        self.spec = spec
        n = spec["planned"]
        c = chunk or (1000 if n <= 20000 else 2000)
        self.chunks = [(s, min(s + c, n)) for s in range(0, n, c)]
        self.next = 0
        self.inflight = 0
        self.ex = X.EarlyStop()
        self.hist, self.rank_r, self.pure_hf, self.examined = {}, 0, 0, 0
        self.members, self.cands, self.nonpure = [], deque(), {}
        self.cpu, self.t0 = 0.0, time.time()
        self.cut = None  # "budget" or "halt" when work was stopped from outside

    def chunks_left(self):
        return 0 if self.ex.stopped else len(self.chunks) - self.next

    def finished(self, closing):
        if self.inflight or self.ex.inflight:
            return False
        if closing or self.chunks_left() == 0 and not (self.cands and self.ex.may_start_table()):
            return True
        return False

    def record(self):
        s = self.spec
        rec = {k: s[k] for k in ("family", "e", "p", "m", "i", "j", "admissible", "d_i", "d_j", "N", "budget", "planned",
                                 "all_members", "enumerated", "seed")}
        rec.update({"examined": self.examined, "complete": self.examined == s["planned"],
                    "stopped_early": self.ex.stopped, "stopped_by": self.cut,
                    "rank_hist": {k: self.hist[k] for k in sorted(self.hist, key=int)}, "rank_r": self.rank_r,
                    "pure_hilbert": self.pure_hf, "tables": self.ex.tables, "pure": self.ex.pure,
                    "tables_cap_reached": self.ex.tables >= X.MAX_TABLES and not self.ex.stopped,
                    "nonpure_tables": self.nonpure, "members_stored": len(self.members),
                    "members": sorted(self.members, key=lambda m: m["index"]),
                    "chunks": [len(self.chunks), self.next], "worker_seconds": round(self.cpu, 1),
                    "wall_seconds": round(time.time() - self.t0, 1)})
        return rec


def _g4_failure(res, st, rec):
    """A member with the pure Hilbert function in a stratum that is not admissible: its polynomials, ranks and Betti table."""
    e, p = rec["e"], rec["p"]
    m0 = rec["members"][0]
    t = X.betti_table(e, p, m0["f"], m0["g"])
    res["gates"]["G4"] = {"passed": False, "stratum": [e, p, rec["m"], rec["i"], rec["j"]], "pure_hilbert_members": rec["pure_hilbert"],
                          "member": {"index": m0["index"], "f": X.poly_text(e, p, m0["f"]), "g": X.poly_text(e, p, m0["g"]),
                                     "ranks": m0["ranks"], "betti": X.table_rows(t), "pure": t == X.pure_table(e)}}


def run_specs(res, specs, workers, chunk=None, deadline=None, save_fn=save, quiet=False):
    """Run the strata of `specs` (in order) on a pool of `workers` processes; store each stratum in res['strata'] when it finishes.
    Chunks of the earliest active stratum go first; the Betti tables of the members with the pure Hilbert function go before chunks; a
    stratum stops handing out chunks once it has 5 pure members (chunks already started finish and are counted).  Returns 1 when
    gate G4 fails (the run stops), else 0."""
    say = (lambda m: None) if quiet else log
    queue = deque(s for s in specs if s["key"] not in res["strata"])
    active, pending = {}, {}
    closing, halted, last_save = False, False, time.time()

    def finalize(st):
        nonlocal halted
        rec = st.record()
        res["strata"][st.spec["key"]] = rec
        say("%s: examined %d of %d, rank r %d, pure Hilbert %d, tables %d, pure %d%s, %.0f s" % (
            st.spec["key"], rec["examined"], rec["planned"], rec["rank_r"], rec["pure_hilbert"], rec["tables"], rec["pure"],
            " (early stop)" if rec["stopped_early"] else (" (cut: %s)" % rec["stopped_by"] if rec["stopped_by"] else ""),
            rec["wall_seconds"]))
        if not rec["admissible"] and rec["pure_hilbert"] and not halted:
            _g4_failure(res, st, rec)
            halted = True
            say("GATE G4 FAILED in %s: a member of a stratum that is not admissible has the pure Hilbert function" % st.spec["key"])

    with ProcessPoolExecutor(max_workers=workers) as pool:
        while queue or active or pending:
            if not closing and deadline is not None and time.time() > deadline:
                closing = True
                say("time budget reached: no further work is handed out")
            if halted:
                closing = True
            # activate strata while the active ones hold too little work to keep the pool busy
            while queue and not closing and len(active) < MAX_ACTIVE and (
                    not active or sum(s.chunks_left() for s in active.values()) < 2 * workers):
                spec = queue.popleft()
                st = Stratum(spec, chunk)
                if spec["planned"] == 0:
                    finalize(st)
                else:
                    active[spec["key"]] = st
            if closing:
                queue.clear()
            # hand out work: Betti tables first, then chunks of the earliest strata
            while len(pending) < workers and not closing:
                job = None
                for st in active.values():
                    if st.cands and st.ex.may_start_table():
                        rec = st.cands.popleft()
                        st.ex.table_started()
                        job = (pool.submit(X.betti_job, {"key": st.spec["key"], "index": rec["index"], "e": st.spec["e"],
                                                         "p": st.spec["p"], "f": rec["f"], "g": rec["g"]}), ("b", st, rec))
                        break
                if job is None:
                    for st in active.values():
                        if st.chunks_left():
                            s, e = st.chunks[st.next]
                            st.next += 1
                            st.inflight += 1
                            job = (pool.submit(X.chunk_job, dict(st.spec, start=s, end=e)), ("c", st, None))
                            break
                if job is None:
                    break
                pending[job[0]] = job[1]
            if pending:
                done, _ = wait(set(pending), timeout=5, return_when=FIRST_COMPLETED)
                for fut in done:
                    kind, st, rec = pending.pop(fut)
                    out = fut.result()
                    if kind == "c":
                        st.inflight -= 1
                        st.examined += out["n"]
                        st.rank_r += out["rank_r"]
                        st.pure_hf += out["pure_hf"]
                        st.cpu += out["seconds"]
                        for k, v in out["rank_hist"].items():
                            st.hist[k] = st.hist.get(k, 0) + v
                        for mem in out["members"]:
                            if len(st.members) < X.MAX_STORED:
                                mem.update({"betti": None, "pure": None})
                                st.members.append(mem)
                                st.cands.append(mem)
                    else:
                        st.ex.table_done(out["pure"])
                        st.cpu += out["seconds"]
                        rec["betti"], rec["pure"] = out["betti"], out["pure"]
                        if not out["pure"]:
                            key = str(out["betti"])
                            st.nonpure[key] = st.nonpure.get(key, 0) + 1
            elif not active and not queue:
                break
            for key in [k for k, st in active.items() if st.finished(closing)]:
                st = active.pop(key)
                if closing and (st.chunks_left() or st.cands):
                    st.cut = "halt" if halted else "budget"
                finalize(st)
            if time.time() - last_save > SAVE_EVERY:
                save_fn(res)
                last_save = time.time()
    save_fn(res)
    return 1 if halted else 0


# ------------------------------------------------------------------ gates G1 (a) to (d) and G3
def _pair_vectors(e, mono_coefs):
    import numpy as np
    from uhlib import algebra as A
    vs = []
    for terms in mono_coefs:
        v = np.zeros(A.dim_U(e), dtype=np.int64)
        for mono, c in terms:
            v[list(A.monos(e)).index(mono)] = c
        vs.append(v)
    return vs


def _in_stratum(e, m, i, j, f, g):
    return all(f[k] == 0 for k in range(len(f)) if k not in X.support(e, m, i)) and all(
        g[k] == 0 for k in range(len(g)) if k not in X.support(e, m, j))


def gate_g1_a():
    rows = []
    for e, p, expect in ((4, 13, True), (5, 13, True), (6, 13, True), (7, 17, True), (4, 5, False)):
        f, g = _pair_vectors(e, [[((e, 0, 0), 1)], [((0, e, 0), 1)]])
        t = X.betti_table(e, p, f, g)
        rows.append({"case": "<x^%d, y^%d> over GF(%d)" % (e, e, p), "betti": X.table_rows(t), "expected_pure": expect,
                     "ok": (t == X.pure_table(e)) is expect})
    return rows


def gate_g1_b():
    rows = []
    for e, p, m, f_terms, g_terms, name in (
            (6, 11, 5, [((6, 0, 0), 1), ((0, 4, 1), 1)], [((0, 6, 0), 1), ((4, 0, 1), 3)], "<x^6 + y^4 z, y^6 + 3 x^4 z> over GF(11)"),
            (7, 13, 6, [((7, 0, 0), 1), ((0, 5, 1), 1)], [((0, 7, 0), 1), ((5, 0, 1), 1)], "<x^7 + y^5 z, y^7 + x^5 z> over GF(13)")):
        f, g = _pair_vectors(e, [f_terms, g_terms])
        t = X.betti_table(e, p, f, g)
        member = _in_stratum(e, m, 0, 1, f, g)
        rows.append({"case": name, "stratum": "S(%d; 0, 1)" % m, "member": member, "betti": X.table_rows(t),
                     "ok": member and t == X.pure_table(e) and X.pure_hilbert_full(e, p, f, g)})
    return rows


def gate_g1_d():
    rows = []
    for e in (4, 5, 6, 7, 8):
        got, note = X.admissible_strata(e), X.note_table(e)
        rows.append({"e": e, "computed": len(got), "note_total": X.NOTE_TOTALS[e], "lists_equal": got == note,
                     "ok": got == note and len(got) == X.NOTE_TOTALS[e]})
    return rows


def gate_g1_c(nworkers):
    jobs = [(e, p, k) for e, p in ((6, 5), (6, 11), (7, 3), (7, 13)) for k in range(50)]
    with ProcessPoolExecutor(max_workers=nworkers) as pool:
        outs = list(pool.map(X.gate_c_case, jobs))
    bad = [o for o in outs if not o["ok"]]
    per_pair = {}
    for o in outs:
        per_pair.setdefault("%d,%d" % (o["e"], o["p"]), []).append(o["ok"])
    return {"cases": len(outs), "per_pair": {k: [len(v), sum(v)] for k, v in per_pair.items()}, "failing_cases": bad[:5],
            "ok": not bad}


def gate_g3():
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_bs_exp010.py", "-q"], cwd=str(ROOT), capture_output=True, text=True)
    tail = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()][-1:]
    return {"passed": proc.returncode == 0, "exit_code": proc.returncode, "last_line": tail[0] if tail else ""}


def gates_ok(res):
    g = res.get("gates", {})
    return g.get("G1", {}).get("direct", {}).get("passed") is True and g.get("G3", {}).get("passed") is True


def cmd_gates():
    ART.mkdir(exist_ok=True)
    res = load()
    t0 = time.time()
    a, b, d = gate_g1_a(), gate_g1_b(), gate_g1_d()
    c = gate_g1_c(workers())
    direct = {"a": a, "b": b, "c": c, "d": d}
    ok = all(r["ok"] for r in a) and all(r["ok"] for r in b) and all(r["ok"] for r in d) and c["ok"]
    g1 = res["gates"].get("G1", {})
    g1["direct"] = dict(direct, passed=ok)
    res["gates"]["G1"] = g1
    save(res)
    log("G1 (a) %s, (b) %s, (c) %s (%d cases), (d) %s" % tuple(["PASSED" if x else "FAILED" for x in (
        all(r["ok"] for r in a), all(r["ok"] for r in b))] + ["PASSED" if c["ok"] else "FAILED", c["cases"]] + [
        "PASSED" if all(r["ok"] for r in d) else "FAILED"]))
    failed = None if ok else "G1"
    if ok:
        g3 = gate_g3()
        res["gates"]["G3"] = g3
        save(res)
        log("G3 %s: %s" % ("PASSED" if g3["passed"] else "FAILED", g3["last_line"]))
        if not g3["passed"]:
            failed = "G3"
    res["runs"].append({"command": "gates", "seconds": round(time.time() - t0, 1)})
    save(res)
    if failed:
        log("GATE FAILED: %s; the run stops here" % failed)
        return 1
    log("G1 (before the families) and G3 passed; the part of G1 after family C and G4 are checked by `cases --family C`; G2 by `second`")
    return 0


def g1_after_c(res):
    """The known answers after family C (hypothesis, gate G1 second part), from the stored strata."""
    def st(e, p, m, i, j):
        return res["strata"].get("C|%d|%d|%d|%d|%d" % (e, p, m, i, j))

    rows = []

    def need_pure(e, p, m, i, j):
        s = st(e, p, m, i, j)
        rows.append({"pair": [e, p], "stratum": "S(%d; %d, %d)" % (m, i, j), "expect": "pure members", "pure": None if s is None else s["pure"],
                     "ok": bool(s and s["pure"] > 0)})

    def need_no_hf(e, p, m, i, j):
        s = st(e, p, m, i, j)
        rows.append({"pair": [e, p], "stratum": "S(%d; %d, %d)" % (m, i, j), "expect": "no member with the pure Hilbert function",
                     "pure_hilbert": None if s is None else s["pure_hilbert"], "examined": None if s is None else s["examined"],
                     "ok": bool(s and s["pure_hilbert"] == 0 and s["examined"] > 0)})

    need_pure(5, 5, 2, 0, 1)
    need_pure(5, 5, 3, 0, 2)
    need_no_hf(5, 5, 4, 0, 1)
    for m, i, j in ((2, 0, 1), (3, 0, 2), (4, 0, 1)):
        need_pure(5, 7, m, i, j)
    need_pure(6, 3, 2, 0, 1)
    for e, p in ((6, 11), (7, 11), (7, 13)):
        need_pure(e, p, e - 1, 0, 1)
    return {"passed": all(r["ok"] for r in rows), "rows": rows}


def g4_after_c(res):
    strata = [s for s in res["strata"].values() if s["family"] == "C" and not s["admissible"]]
    bad = [s for s in strata if s["pure_hilbert"]]
    return {"passed": not bad and "member" not in res["gates"].get("G4", {}), "strata_not_admissible": len(strata),
            "members_examined": sum(s["examined"] for s in strata), "with_pure_hilbert_function": sum(s["pure_hilbert"] for s in strata)}


# ------------------------------------------------------------------ cases
def cmd_cases():
    res = load()
    if not gates_ok(res):
        log("G1 (before the families) and G3 have not both passed; run `gates` first")
        return 1
    fam = opt("family", "")
    if fam not in X.FAMILIES:
        log("--family C|Q|E is required")
        return 2
    if fam in ("Q", "E"):
        g = res["gates"]
        if not (g.get("G1", {}).get("after_c", {}).get("passed") and g.get("G4", {}).get("passed")):
            log("family C has not passed G4 and the control part of G1; run `cases --family C` first")
            return 1
    only = pair_list()
    specs = X.plan_family(fam, only)
    remaining = [s for s in specs if s["key"] not in res["strata"]]
    used = res["budget"]["used_seconds"]
    left = float(opt("budget-seconds", BUDGET_SECONDS - used))
    t0 = time.time()
    log("family %s: %d strata planned, %d to do; budget left %.0f s (used %.0f s of %d s)" % (fam, len(specs), len(remaining), left, used,
                                                                                         BUDGET_SECONDS))
    rc = run_specs(res, remaining, workers(), chunk=int(opt("chunk", 0)) or None, deadline=t0 + left)
    dt = time.time() - t0
    res["budget"]["used_seconds"] = round(res["budget"]["used_seconds"] + dt, 1)
    res["runs"].append({"command": "cases", "family": fam, "only": opt("only", None), "seconds": round(dt, 1), "stopped_by_gate": rc == 1})
    if fam == "C" and rc == 0 and all(s["key"] in res["strata"] for s in X.plan_family("C")):
        res["gates"]["G4"] = g4_after_c(res)
        res["gates"]["G1"]["after_c"] = g1_after_c(res)
        log("G4 %s: %s" % ("PASSED" if res["gates"]["G4"]["passed"] else "FAILED", json.dumps(res["gates"]["G4"])))
        log("G1 (after family C) %s" % ("PASSED" if res["gates"]["G1"]["after_c"]["passed"] else "FAILED: " + json.dumps(
            [r for r in res["gates"]["G1"]["after_c"]["rows"] if not r["ok"]])))
        rc = 0 if res["gates"]["G4"]["passed"] and res["gates"]["G1"]["after_c"]["passed"] else 1
    save(res)
    done = sum(1 for s in specs if s["key"] in res["strata"])
    log("family %s: %d of %d strata stored; %.0f s this run, %.0f s in total" % (fam, done, len(specs), dt, res["budget"]["used_seconds"]))
    return rc


# ------------------------------------------------------------------ G2: the second instrument
def singular_available():
    try:
        p = subprocess.run(["wsl", "-e", "bash", "-c", "Singular -v < /dev/null | head -1"], capture_output=True, text=True, timeout=120)
    except Exception as exc:
        return False, repr(exc)[:200]
    lines = [ln for ln in p.stdout.splitlines() if "Singular" in ln]
    return p.returncode == 0 and bool(lines), lines[0].strip() if lines else p.stderr[:200]


def g2_sample(res):
    """The first two pure members of every stratum that has one, strata in decreasing m, at most ten members per pair."""
    out, per_pair = [], {}
    for key, s in sorted(res["strata"].items(), key=lambda kv: (kv[1]["e"], kv[1]["p"], -kv[1]["m"], kv[1]["i"], kv[1]["j"], kv[0])):
        pair = (s["e"], s["p"])
        for mem in [m for m in s["members"] if m["pure"]][:G2_PER_STRATUM]:
            if per_pair.get(pair, 0) < G2_PER_PAIR:
                per_pair[pair] = per_pair.get(pair, 0) + 1
                out.append((key, mem))
    return out


def cmd_second():
    import exp009_singular as Sg
    res = load()
    t0 = time.time()
    if not gates_ok(res):
        log("G1 (before the families) and G3 have not both passed; run `gates` first")
        return 1
    ok, version = singular_available()
    if not ok:
        res["gates"]["G2"] = {"passed": False, "blocked": True, "reason": "Singular is not available through WSL: " + version,
                              "note": "single-instrument results"}
        save(res)
        log("G2 BLOCKED: " + version)
        return 1
    out_dir = Path(opt("out-dir", str(ART / "singular_out")))
    out_dir.mkdir(parents=True, exist_ok=True)
    SING.mkdir(parents=True, exist_ok=True)
    sample = g2_sample(res)
    log("G2: %d pure members in the sample (%s)" % (len(sample), version))

    def one(item):
        key, mem = item
        s = res["strata"][key]
        e, p = s["e"], s["p"]
        name = "e%d_p%d_m%d_%d_%d_idx%d" % (e, p, s["m"], s["i"], s["j"], mem["index"])
        field = {"name": "GF(%d)" % p, "uhlib_name": "GF(%d)" % p, "char": p, "degree": 1, "modulus": None}
        return name, Sg.run_member(name, field, X.basis_json(e, p, mem["f"], mem["g"]), out_dir)

    with ThreadPoolExecutor(max_workers=min(8, workers())) as tp:
        outs = list(tp.map(one, sample))
    rows, bad, errors = [], [], []
    for (key, mem), (name, (t, dt, err)) in zip(sample, outs):
        s = res["strata"][key]
        e = s["e"]
        row = {"stratum": key, "index": mem["index"], "script": name + ".sing", "seconds": round(dt, 1), "betti_I1": mem["betti"]}
        if err or t is None:
            row["error"] = err
            errors.append(name)
        else:
            row["betti_I2"] = [[i, j, r] for (i, j), r in sorted(t.items())]
            row["agree"] = [tuple(x) for x in mem["betti"]] == [tuple(x) for x in row["betti_I2"]]
            row["pure_I2"] = t == X.pure_table(e)
            if not (row["agree"] and row["pure_I2"]):
                bad.append(name)
        rows.append(row)
        src = out_dir / (name + ".sing")
        if src.exists():
            shutil.copyfile(src, SING / (name + ".sing"))
    agree = sum(1 for r in rows if r.get("agree") and r.get("pure_I2"))
    res["gates"]["G2"] = {"passed": not bad and not errors, "singular": version, "sample_members": len(sample), "agree_and_pure_in_I2": agree,
                          "failing_cases": bad, "singular_errors": errors, "rows": rows}
    res["runs"].append({"command": "second", "seconds": round(time.time() - t0, 1)})
    save(res)
    g = res["gates"]["G2"]
    log("G2 %s: %d of %d agree and are pure in both instruments; failing %s; errors %s" % ("PASSED" if g["passed"] else "FAILED", agree,
                                                                                       len(sample), bad[:5], errors[:5]))
    return 0 if g["passed"] else 1


# ------------------------------------------------------------------ table
def _make_summary():
    spec = importlib.util.spec_from_file_location("exp010_make_summary", HERE / "make_summary.py")
    ms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ms)
    return ms


def cmd_table():
    ms = _make_summary()
    res = load()
    res["totals"] = ms.compute_totals(res)
    res["predictions"] = ms.predictions(res, res["totals"])
    res["wall_seconds_total"] = round(sum(r["seconds"] for r in res["runs"]), 1)
    save(res)
    print(ms.totals_text(res["totals"]))
    ms.write_summary(res, HERE / "results-summary.md")
    log("table written")
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    ART.mkdir(exist_ok=True)
    fn = {"gates": cmd_gates, "cases": cmd_cases, "second": cmd_second, "table": cmd_table}.get(cmd)
    if fn is None:
        print(__doc__)
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
