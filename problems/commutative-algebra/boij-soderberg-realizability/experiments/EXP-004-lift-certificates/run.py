"""EXP-004 driver: rank certificates for the lift of EXP-001's prime-field realizations to characteristic 0.

Run from the repository root with the repo .venv. The data root is --data-root or the environment variable
CAOS_RESEARCH_DATA (never a path in the code). Per-hit logs go to <data root>/boij-soderberg-realizability/EXP-004/.
The frozen hypothesis is hypothesis.md in this folder; the construction is liftcert.py.

    run.py gates    G4 (the unit tests) and G1 (ranks mod p reproduce the pure Hilbert function) on every hit
    run.py known    G2: the hits that EXP-001 resolved over QQ with the pure table; stops at the first failure
    run.py rest     the other hits
    run.py second   the PARI/GP instrument (WSL) on every matrix with at most 2,000 rows and a fixed sample of larger ones: G3
    run.py table    artifacts/results.json and results-summary.md from the logs

Every process started is waited for (or terminated through its own handle at its limit); each finished hit is one
appended JSON line, so a rerun skips finished work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import queue
import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
import liftcert as L  # noqa: E402

ARTIFACTS = HERE / "artifacts"
SRC_SUBDIR = Path("boij-soderberg-realizability") / "EXP-001"
OUT_SUBDIR = Path("boij-soderberg-realizability") / "EXP-004"
MANIFEST = HERE.parent / "EXP-001-pure-ray-census" / "artifacts" / "hits-manifest.json"
EXP001_RESULTS = HERE.parent / "EXP-001-pure-ray-census" / "artifacts" / "results.json"
QQ_LIMIT = 1200          # seconds per matrix for the rank over QQ (hypothesis)
GP_LIMIT = 1200          # seconds per matrix for PARI/GP
MAX_WORKERS = 8          # hypothesis: at most 8 processes
SECOND_ROWS = 2000       # second instrument on every matrix with at most this many rows
SECOND_SAMPLE = 20       # and on a fixed-seed sample of this many larger ones
SAMPLE_SEED = 20261119
P3_TAGS = ("0-3-8-10_m1_module_s1_p32003", "0-3-11-12_m1_module_s1_p32003")
DATA_ROOT_TEXT = ""      # replaced in logs by "<data root>"


# ------------------------------------------------------------------------------------------------ helpers

def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    if DATA_ROOT_TEXT:
        line = line.replace(DATA_ROOT_TEXT, "<data root>")
    print(line, flush=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with open(ARTIFACTS / "run.log", "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def resolve_root(args) -> Path:
    root = args.data_root or os.environ.get("CAOS_RESEARCH_DATA")
    if not root:
        sys.exit("stop: pass --data-root or set CAOS_RESEARCH_DATA (the data root, parent of boij-soderberg-realizability)")
    global DATA_ROOT_TEXT
    DATA_ROOT_TEXT = str(root).replace("\\", "/")
    return Path(root)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def append_jsonl(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")


class Ctx:
    def __init__(self, root: Path):
        self.root = root
        self.src = root / SRC_SUBDIR
        self.out = root / OUT_SUBDIR
        self.out.mkdir(parents=True, exist_ok=True)
        self.g1_file = self.out / "g1.jsonl"
        self.deg_file = self.out / "degrees.jsonl"
        self.hit_file = self.out / "hits.jsonl"
        self.second_file = self.out / "second.jsonl"
        self.skipped_file = self.out / "skipped.json"
        self.g4_file = self.out / "g4.json"
        self.gates_file = self.out / "gates.json"


def load_hits(ctx: Ctx) -> tuple[list[dict], list[dict]]:
    """The verified hits (the tags of EXP-001's verify.jsonl, last record per tag) with their manifest entry,
    SHA-256 checked. Returns (usable hits, skipped with the reason). A hit file that is missing or whose hash does
    not match the manifest is skipped (never regenerated)."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_tag = {}
    for h in manifest["hits"]:
        for f in h["files"]:
            if f["path"].endswith(".hit.m2"):
                by_tag[Path(f["path"]).name[: -len(".hit.m2")]] = (h, f)
    verify = {}
    for rec in read_jsonl(ctx.src / "verify.jsonl"):
        verify[rec["tag"]] = rec
    hits, skipped = [], []
    for tag in sorted(verify):
        rec = verify[tag]
        if tag not in by_tag:
            skipped.append({"tag": tag, "reason": "not in the manifest"})
            continue
        _, f = by_tag[tag]
        path = ctx.src / f["path"]
        if not path.exists():
            skipped.append({"tag": tag, "reason": "hit file missing"})
            continue
        if sha256(path) != f["sha256"]:
            skipped.append({"tag": tag, "reason": "SHA-256 differs from the manifest"})
            continue
        hits.append({"tag": tag, "path": str(path), "exp001": rec.get("qq", {}).get("status", "not run"),
                     "d": tuple(rec["d"]), "m": rec["m"], "gen": rec["gen"], "p": rec["p"]})
    return hits, skipped


def load_parsed(hit: dict):
    parsed = L.parse_hit_text(Path(hit["path"]).read_text(encoding="utf-8"))
    plan = L.degree_plan(parsed)
    if len(parsed.F) != plan["F_rows"] or len(parsed.F[0]) != plan["F_cols"]:
        raise ValueError(f"{hit['tag']}: hitF is {len(parsed.F)} x {len(parsed.F[0])}, expected "
                         f"{plan['F_rows']} x {plan['F_cols']}")
    if (parsed.d, parsed.m, parsed.gen, parsed.p) != (hit["d"], hit["m"], hit["gen"], hit["p"]):
        raise ValueError(f"{hit['tag']}: header differs from verify.jsonl")
    return parsed, plan


def build(parsed, plan, degree: int) -> L.Mat:
    F = L.lift_matrix(parsed.F, parsed.p)
    if parsed.gen == "module":
        return L.build_form_a(F, plan["col_degs"], degree)
    return L.build_form_b(F, plan["r"], plan["e"], degree)


def degrees_of(plan) -> range:
    return range(plan["top"] + 2)      # 0 .. top + 1 (the Hilbert function is 0 at top + 1)


def expected_dim(parsed, plan, degree: int) -> int:
    h = L.hilbert_pure(parsed.d, parsed.m)
    return h[degree] if degree < len(h) else 0


def dim_from_rank(parsed, mat: L.Mat, rank: int) -> int:
    return mat.rows - rank if parsed.gen == "module" else rank


# ------------------------------------------------------------------------------------------------ worker tasks

def _child(qu, hit: dict, degree: int, mode: str) -> None:
    try:
        parsed, plan = load_parsed(hit)
        mat = build(parsed, plan, degree)
        t0 = time.time()
        rp = L.rank_mod_p(mat, parsed.p)
        qu.put({"kind": "p", "rows": mat.rows, "cols": mat.cols, "rank_p": rp,
                "dim_p": dim_from_rank(parsed, mat, rp), "seconds_p": round(time.time() - t0, 3)})
        if mode == "q":
            t1 = time.time()
            rq = L.rank_qq(mat)
            qu.put({"kind": "q", "rank_qq": rq, "seconds_qq": round(time.time() - t1, 3)})
    except Exception as exc:  # reported, never swallowed
        qu.put({"kind": "error", "error": f"{type(exc).__name__}: {exc}"})


def run_degree_tasks(tasks: list[dict], hits_by_tag: dict, mode: str, limit: float, workers: int, out_file: Path,
                     on_record) -> None:
    """Run (tag, degree) tasks with at most `workers` processes of this script; a task that exceeds `limit`
    seconds in the rank over QQ is terminated through its own handle and recorded as undecided. `on_record` is
    called with every finished record and returns True to stop launching further tasks."""
    ctx_mp = mp.get_context("spawn")
    pending = list(tasks)
    running: list[dict] = []
    stop = False
    while pending or running:
        while pending and len(running) < workers and not stop:
            t = pending.pop(0)
            qu = ctx_mp.Queue()
            proc = ctx_mp.Process(target=_child, args=(qu, hits_by_tag[t["tag"]], t["degree"], mode))
            proc.start()
            running.append({"t": t, "q": qu, "proc": proc, "start": time.time(), "p": None, "q_res": None,
                            "error": None})
        if not running:
            break
        time.sleep(0.2)
        for r in list(running):
            while True:
                try:
                    msg = r["q"].get_nowait()
                except queue.Empty:
                    break
                if msg["kind"] == "p":
                    r["p"] = msg
                    r["p_time"] = time.time()
                elif msg["kind"] == "q":
                    r["q_res"] = msg
                else:
                    r["error"] = msg["error"]
            alive = r["proc"].is_alive()
            finished = (not alive) or r["error"] is not None
            timed_out = False
            if alive and mode == "q":
                t_start = r.get("p_time", r["start"])
                timed_out = (time.time() - t_start) > limit
            if not (finished or timed_out):
                continue
            if alive:
                r["proc"].terminate()
            r["proc"].join(timeout=60)
            if r["proc"].is_alive():
                r["proc"].kill()
                r["proc"].join()
            while True:                   # final drain after the process ended
                try:
                    msg = r["q"].get(timeout=0.5)
                except queue.Empty:
                    break
                if msg["kind"] == "p":
                    r["p"] = msg
                elif msg["kind"] == "q":
                    r["q_res"] = msg
                else:
                    r["error"] = msg["error"]
            r["q"].close()
            running.remove(r)
            rec = {"tag": r["t"]["tag"], "degree": r["t"]["degree"]}
            if r["p"]:
                rec.update({k: r["p"][k] for k in ("rows", "cols", "rank_p", "dim_p", "seconds_p")})
            if mode == "q":
                if r["q_res"]:
                    rec.update({"rank_qq": r["q_res"]["rank_qq"], "seconds_qq": r["q_res"]["seconds_qq"],
                                "status": "ok"})
                elif r["error"] or not r["p"]:
                    rec.update({"status": "error", "error": r["error"] or f"exit {r['proc'].exitcode}"})
                else:
                    rec.update({"status": "undecided", "reason": f"rank over QQ exceeded {int(limit)} s"})
            else:
                if not r["p"]:
                    rec.update({"status": "error", "error": r["error"] or f"exit {r['proc'].exitcode}"})
                else:
                    rec["status"] = "ok"
            append_jsonl(out_file, rec)
            if on_record(rec):
                stop = True
    if stop:
        log("stopping: no further tasks launched")


# ------------------------------------------------------------------------------------------------ evaluation

def evaluate_hit(hit: dict, recs: dict[int, dict]) -> dict:
    """The result record of one hit from its per-degree records (degree -> record)."""
    parsed, plan = load_parsed(hit)
    top = plan["top"]
    hf = L.hilbert_pure(parsed.d, parsed.m)
    degs, larger, undecided, g1_bad = [], [], [], []
    seconds = 0.0
    for d in degrees_of(plan):
        r = recs.get(d)
        want = hf[d] if d < len(hf) else 0
        if r is None:
            undecided.append(d)
            continue
        item = {"degree": d, "rows": r.get("rows"), "cols": r.get("cols"), "rank_p": r.get("rank_p"),
                "rank_qq": r.get("rank_qq"), "hilbert": want,
                "seconds_p": r.get("seconds_p"), "seconds_qq": r.get("seconds_qq"), "status": r.get("status")}
        seconds += (r.get("seconds_p") or 0) + (r.get("seconds_qq") or 0)
        if r.get("dim_p") is not None and r["dim_p"] != want:
            g1_bad.append(d)
        if r.get("rank_qq") is None:
            undecided.append(d)
        elif r["rank_qq"] > r["rank_p"]:
            larger.append(d)
        elif r["rank_qq"] < r["rank_p"]:
            g1_bad.append(d)            # impossible for exact ranks: reported as a defect
        degs.append(item)
    verdict = "fail" if larger else ("undecided" if undecided else "pass")
    return {"tag": hit["tag"], "d": list(parsed.d), "m": parsed.m, "gen": parsed.gen, "p": parsed.p,
            "top": top, "hilbert_pure": hf, "degrees": degs, "verdict": verdict,
            "degrees_rank_qq_larger": larger, "degrees_undecided": undecided, "g1_degrees_wrong": g1_bad,
            "exp001_qq": hit["exp001"], "seconds": round(seconds, 2),
            "max_shape": max(((x["rows"] or 0, x["cols"] or 0) for x in degs), key=lambda s: s[0] * s[1],
                             default=(0, 0))}


def run_stage(ctx: Ctx, hits: list[dict], label: str, stop_on_nonpass: bool, workers: int, limit: float) -> int:
    hits_by_tag = {h["tag"]: h for h in hits}
    done = {r["tag"] for r in read_jsonl(ctx.hit_file)}
    todo = [h for h in hits if h["tag"] not in done]
    log(f"{label}: {len(hits)} hits, {len(done & set(hits_by_tag))} finished, {len(todo)} to run, "
        f"{workers} workers, limit {int(limit)} s per rank over QQ")
    recs: dict[str, dict[int, dict]] = {}
    for r in read_jsonl(ctx.deg_file):
        recs.setdefault(r["tag"], {})[r["degree"]] = r
    tasks = []
    for h in todo:
        parsed, plan = load_parsed(h)
        for d in degrees_of(plan):
            have = recs.get(h["tag"], {}).get(d)
            if have and have.get("status") in ("ok", "undecided"):
                continue
            mat_rows = size_hint(parsed, plan, d)
            tasks.append({"tag": h["tag"], "degree": d, "size": mat_rows})
    tasks.sort(key=lambda t: -t["size"])
    ndeg = {h["tag"]: len(list(degrees_of(load_parsed(h)[1]))) for h in todo}
    failed: list[str] = []
    state = {"stop": False}

    def on_record(rec) -> bool:
        recs.setdefault(rec["tag"], {})[rec["degree"]] = rec
        t = rec["tag"]
        if rec.get("status") == "error":
            log(f"ERROR {t} degree {rec['degree']}: {rec.get('error')}")
        if len(recs[t]) == ndeg[t]:
            res = evaluate_hit(hits_by_tag[t], recs[t])
            append_jsonl(ctx.hit_file, res)
            log(f"{t}: {res['verdict']} (EXP-001 QQ status {res['exp001_qq']}; largest matrix "
                f"{res['max_shape'][0]}x{res['max_shape'][1]}; {res['seconds']} s)")
            if stop_on_nonpass and res["verdict"] != "pass":
                failed.append(t)
                log(f"STOP: {t} did not pass ({res['verdict']}; larger in degrees {res['degrees_rank_qq_larger']}, "
                    f"undecided {res['degrees_undecided']}); no further task is launched")
                state["stop"] = True
        return state["stop"]

    # already complete hits whose lines were not written (a kill between the last degree and the line)
    for h in todo:
        if h["tag"] in recs and len(recs[h["tag"]]) == ndeg[h["tag"]] and all(
                recs[h["tag"]][d].get("status") in ("ok", "undecided") for d in recs[h["tag"]]):
            on_record(recs[h["tag"]][max(recs[h["tag"]])])
    tasks = [t for t in tasks if t["tag"] not in failed]
    run_degree_tasks(tasks, hits_by_tag, "q", limit, workers, ctx.deg_file, on_record)
    return 1 if failed else 0


def size_hint(parsed, plan, degree: int) -> int:
    from math import comb
    if parsed.gen == "module":
        d1 = parsed.d[1]
        rows = plan["F_rows"] * comb(degree + 2, 2)
        cols = plan["F_cols"] * (comb(degree - d1 + 2, 2) if degree >= d1 else 0)
    else:
        rows = plan["F_rows"] * len(L.monomials_t(degree + plan["e"], plan["r"]))
        cols = plan["F_cols"] * len(L.monomials_t(degree, plan["r"]))
    return rows * cols


# ------------------------------------------------------------------------------------------------ gates

def cmd_gates(args) -> int:
    ctx = Ctx(resolve_root(args))
    hits, skipped = load_hits(ctx)
    ctx.skipped_file.write_text(json.dumps(skipped, indent=1), encoding="utf-8")
    log(f"hits: {len(hits)} usable, {len(skipped)} skipped {skipped if skipped else ''}")
    # G4: the unit tests, in a process waited for
    cp = subprocess.run([sys.executable, "-m", "pytest", "-o", "addopts=", str(HERE.parents[4] / "tests" / "test_bs_liftcert.py"), "-q"],
                        capture_output=True, text=True, cwd=str(HERE.parents[4]), timeout=900)
    tail = cp.stdout.strip().splitlines()[-1] if cp.stdout.strip() else ""
    g4 = {"passed": cp.returncode == 0, "summary": tail}
    ctx.g4_file.write_text(json.dumps(g4), encoding="utf-8")
    log(f"G4 {'passed' if g4['passed'] else 'FAILED'}: {tail}")
    if not g4["passed"]:
        print(cp.stdout[-3000:])
        return 1
    # G1: ranks mod p against the pure Hilbert function
    hits_by_tag = {h["tag"]: h for h in hits}
    have = {(r["tag"], r["degree"]) for r in read_jsonl(ctx.g1_file) if r.get("status") == "ok"}
    tasks = []
    for h in hits:
        parsed, plan = load_parsed(h)
        for d in degrees_of(plan):
            if (h["tag"], d) not in have:
                tasks.append({"tag": h["tag"], "degree": d, "size": size_hint(parsed, plan, d)})
    tasks.sort(key=lambda t: -t["size"])
    log(f"G1: {len(tasks)} matrices to reduce mod p ({args.workers} workers)")
    bad: list[str] = []

    def on_record(rec) -> bool:
        if rec.get("status") != "ok":
            bad.append(f"{rec['tag']} degree {rec['degree']}: {rec.get('error')}")
        return False

    run_degree_tasks(tasks, hits_by_tag, "p", 0, min(args.workers, MAX_WORKERS), ctx.g1_file, on_record)
    recs: dict[str, dict[int, dict]] = {}
    for r in read_jsonl(ctx.g1_file):
        recs.setdefault(r["tag"], {})[r["degree"]] = r
    failures = []
    n_matrices = 0
    for h in hits:
        parsed, plan = load_parsed(h)
        hf = L.hilbert_pure(parsed.d, parsed.m)
        for d in degrees_of(plan):
            r = recs.get(h["tag"], {}).get(d)
            want = hf[d] if d < len(hf) else 0
            if r is None or r.get("status") != "ok":
                failures.append((h["tag"], d, "no rank mod p", want))
                continue
            n_matrices += 1
            if r["dim_p"] != want:
                failures.append((h["tag"], d, r["dim_p"], want))
    gen_fail = {}
    for tag, *_ in failures:
        gen_fail.setdefault(hits_by_tag[tag]["gen"], set()).add(tag)
    g1 = {"passed": not failures, "hits": len(hits), "matrices": n_matrices, "failures": failures[:50],
          "failed_by_generator": {k: sorted(v) for k, v in gen_fail.items()}}
    ctx.gates_file.write_text(json.dumps({"G1": g1, "G4": g4}, indent=1), encoding="utf-8")
    if failures:
        tag, d, got, want = failures[0]
        log(f"G1 FAILED on {tag} degree {d}: dim {got}, pure Hilbert function {want}; failing hits by generator "
            f"{ {k: len(v) for k, v in gen_fail.items()} }. Fix the construction against recheck.m2; "
            f"the gate is not relaxed.")
        return 1
    log(f"G1 passed: {n_matrices} matrices of {len(hits)} hits, the ranks mod p reproduce the pure Hilbert function "
        f"in every degree 0..top+1")
    return 0


# ------------------------------------------------------------------------------------------------ known and rest

def cmd_known(args) -> int:
    ctx = Ctx(resolve_root(args))
    hits, _ = load_hits(ctx)
    known = [h for h in hits if h["exp001"] == "ok"]
    log(f"G2 (known answers): {len(known)} hits with EXP-001 QQ status ok")
    rc = run_stage(ctx, known, "known", True, min(args.workers, MAX_WORKERS), args.limit)
    res = {r["tag"]: r for r in read_jsonl(ctx.hit_file)}
    n_pass = sum(1 for h in known if res.get(h["tag"], {}).get("verdict") == "pass")
    log(f"G2: {n_pass} of {len(known)} known hits pass the rank test in every degree")
    return rc if n_pass != len(known) else 0


def cmd_rest(args) -> int:
    ctx = Ctx(resolve_root(args))
    hits, _ = load_hits(ctx)
    res = {r["tag"]: r for r in read_jsonl(ctx.hit_file)}
    known = [h for h in hits if h["exp001"] == "ok"]
    if any(res.get(h["tag"], {}).get("verdict") != "pass" for h in known):
        log("stop: G2 (known) has not passed on every known hit; run `known` first")
        return 1
    rest = [h for h in hits if h["exp001"] != "ok"]
    log(f"rest: {len(rest)} hits without a completed positive recheck")
    run_stage(ctx, rest, "rest", False, min(args.workers, MAX_WORKERS), args.limit)
    return 0


# ------------------------------------------------------------------------------------------------ second instrument

def run_gp(path: Path, timeout: float) -> tuple[dict | None, float, str]:
    wpath = path.as_posix()
    if len(wpath) > 1 and wpath[1] == ":":
        wpath = f"/mnt/{wpath[0].lower()}{wpath[2:]}"
    t0 = time.time()
    proc = subprocess.Popen(["wsl", "-e", "bash", "-c", f"timeout {int(timeout)} gp -q -f '{wpath}' < /dev/null"],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    try:
        out, _ = proc.communicate(timeout=timeout + 120)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return None, time.time() - t0, "timeout"
    vals = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0] in ("rankQQ", "rankP") and parts[1].lstrip("-").isdigit():
            vals[parts[0]] = int(parts[1])
    if "rankQQ" in vals and "rankP" in vals:
        return vals, time.time() - t0, "ok"
    return None, time.time() - t0, f"no result (exit {proc.returncode})"


def cmd_second(args) -> int:
    ctx = Ctx(resolve_root(args))
    hits, _ = load_hits(ctx)
    hits_by_tag = {h["tag"]: h for h in hits}
    recs = [r for r in read_jsonl(ctx.deg_file) if r.get("status") in ("ok", "undecided") and r.get("rows")
            and r.get("cols") and r["tag"] in hits_by_tag]
    small = sorted((r for r in recs if r["rows"] <= SECOND_ROWS), key=lambda r: (r["tag"], r["degree"]))
    large = sorted((r for r in recs if r["rows"] > SECOND_ROWS), key=lambda r: (r["tag"], r["degree"]))
    sample = random.Random(SAMPLE_SEED).sample(large, min(SECOND_SAMPLE, len(large)))
    chosen = small + sorted(sample, key=lambda r: (r["tag"], r["degree"]))
    done = {(r["tag"], r["degree"]) for r in read_jsonl(ctx.second_file)}
    todo = [r for r in chosen if (r["tag"], r["degree"]) not in done]
    gp_dir = ctx.out / "gp"
    gp_dir.mkdir(exist_ok=True)
    log(f"second instrument: {len(chosen)} matrices selected ({len(small)} with at most {SECOND_ROWS} rows, "
        f"{len(sample)} sampled from {len(large)} larger, seed {SAMPLE_SEED}); {len(todo)} to run")
    todo.sort(key=lambda r: -(r["rows"] * r["cols"]))
    workers = min(args.workers, MAX_WORKERS)
    import concurrent.futures as cf

    def job(r):
        parsed, plan = load_parsed(hits_by_tag[r["tag"]])
        mat = build(parsed, plan, r["degree"])
        gp = gp_dir / f"{r['tag']}_d{r['degree']}.gp"
        gp.write_text(L.gp_text(mat, parsed.p) + "quit;\n", encoding="utf-8")
        vals, secs, status = run_gp(gp, args.gp_limit)
        try:
            gp.unlink()
        except OSError:
            pass
        rec = {"tag": r["tag"], "degree": r["degree"], "rows": mat.rows, "cols": mat.cols, "status": status,
               "seconds": round(secs, 2), "sampled": r["rows"] > SECOND_ROWS}
        if vals:
            fq = r.get("rank_qq")          # None when python-flint hit its time limit: nothing to compare
            rec.update({"gp_rank_qq": vals["rankQQ"], "gp_rank_p": vals["rankP"],
                        "flint_rank_qq": fq, "flint_rank_p": r["rank_p"],
                        "agree": None if fq is None else (vals["rankQQ"] == fq and vals["rankP"] == r["rank_p"])})
        return rec

    bad = 0
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:   # each job waits for its own wsl process
        for rec in ex.map(job, todo):
            append_jsonl(ctx.second_file, rec)
            if rec["status"] != "ok" or rec.get("agree") is False:
                bad += 1
                log(f"second: {rec['tag']} degree {rec['degree']}: {rec['status']} agree={rec.get('agree')}")
    log(f"second instrument finished: {len(todo)} run, {bad} not agreeing or not finished")
    return 0


# ------------------------------------------------------------------------------------------------ table

def ray_scope_tables(new_char0: list[dict]) -> dict:
    """Rays realized over GF(32003) only in EXP-001's results.json, and which become realized in characteristic 0
    by a passing hit at multiple 1 (directly, and through census.compute_tables with the passing hits added as
    characteristic 0 realizations, which adds duality and the closures EXP-001 uses)."""
    res = json.loads(EXP001_RESULTS.read_text(encoding="utf-8"))
    char0_fields = {"characteristic 0", "any field", "infinite field"}
    only_p = []
    for ray in res["rays"]:
        ents = ray["realized"].get("1", [])
        if ents and not any(e["field"] in char0_fields for e in ents):
            only_p.append(tuple(ray["d"]))
    passing = {tuple(h["d"]) for h in new_char0 if h["m"] == 1}
    direct = sorted(d for d in only_p if d in passing)
    out = {"only_gf32003_rays": len(only_p), "become_char0_by_passing_hit_at_m1": [list(d) for d in direct],
           "become_char0_count": len(direct)}
    try:
        sys.path.insert(0, str(L.EXP001))
        import census as C
        extra = []
        for ray in res["rays"]:
            for m, ents in ray["realized"].items():
                for e in ents:
                    if e["route"].startswith("search:") or e["route"].startswith("QQ recheck"):
                        extra.append({"d": tuple(ray["d"]), "m": int(m), "route": e["route"], "field": e["field"],
                                      "stage": "", "evidence": e["evidence"]})
        base = C.counts(C.compute_tables(extra_realized=extra))
        added = [{"d": tuple(h["d"]), "m": h["m"], "route": "EXP-004 rank certificate", "field": C.CHAR0,
                  "stage": "", "evidence": "rank test"} for h in new_char0]
        after = C.counts(C.compute_tables(extra_realized=extra + added))
        out["census_closure"] = {"reproduces_exp001_char0": base["primitive_realized_char0"],
                                 "char0_before": base["primitive_realized_char0"],
                                 "char0_after": after["primitive_realized_char0"],
                                 "realized_before": base["primitive_realized"],
                                 "realized_after": after["primitive_realized"]}
        # rays that gained char 0 realization through the closures (direct or dual)
        t0 = C.compute_tables(extra_realized=extra)
        t1 = C.compute_tables(extra_realized=extra + added)

        def char0_ok(tab, d):
            ents = tab[d]["realized"].get(1, tab[d]["realized"].get("1", []))
            return any(e["field"] in char0_fields for e in ents)

        gained = sorted(d for d in only_p if char0_ok(t1, d) and not char0_ok(t0, d))
        out["become_char0_with_closures"] = [list(d) for d in gained]
        out["become_char0_with_closures_count"] = len(gained)
    except Exception as exc:  # reported in the results, never hidden
        out["census_closure_error"] = f"{type(exc).__name__}: {exc}"
    return out


def cmd_table(args) -> int:
    ctx = Ctx(resolve_root(args))
    hits, skipped = load_hits(ctx)
    res = {r["tag"]: r for r in read_jsonl(ctx.hit_file)}
    rows = [res[h["tag"]] for h in hits if h["tag"] in res]
    missing = [h["tag"] for h in hits if h["tag"] not in res]
    gates = json.loads(ctx.gates_file.read_text(encoding="utf-8")) if ctx.gates_file.exists() else {}
    g1, g4 = gates.get("G1"), gates.get("G4")
    second = read_jsonl(ctx.second_file)
    sec_ok = [r for r in second if r["status"] == "ok"]
    sec_cmp = [r for r in sec_ok if r.get("agree") is not None]
    sec_agree = [r for r in sec_cmp if r["agree"]]
    sec_bad = [r for r in second if r["status"] != "ok" or r.get("agree") is False]
    sec_extra = [r for r in sec_ok if r.get("agree") is None]
    known = [r for r in rows if r["exp001_qq"] == "ok"]
    rest = [r for r in rows if r["exp001_qq"] != "ok"]
    gp_rank = {(r["tag"], r["degree"]): r for r in sec_ok}
    for r in rows:                      # verdict when PARI/GP completes a matrix that python-flint left undecided
        larger2 = list(r["degrees_rank_qq_larger"])
        open2 = []
        for d in r["degrees_undecided"]:
            g = gp_rank.get((r["tag"], d))
            if g is None:
                open2.append(d)
            elif g["gp_rank_qq"] > g["flint_rank_p"]:
                larger2.append(d)
        r["verdict_two_instruments"] = "fail" if larger2 else ("undecided" if open2 else "pass")
        r["degrees_decided_by_second_instrument"] = [d for d in r["degrees_undecided"] if (r["tag"], d) in gp_rank]

    def count(rs):
        return {v: sum(1 for r in rs if r["verdict"] == v) for v in ("pass", "fail", "undecided")}

    by_status = {}
    for st in ("ok", "fail", "timeout", "not run"):
        by_status[st] = count([r for r in rows if r["exp001_qq"] == st]) | {"hits": sum(
            1 for r in rows if r["exp001_qq"] == st)}
    g2 = {"hits": len(known), "pass": sum(1 for r in known if r["verdict"] == "pass")}
    g2["passed"] = bool(known) and g2["pass"] == len(known) and len(known) == sum(
        1 for h in hits if h["exp001"] == "ok")
    g3 = {"compared": len(sec_cmp), "agree": len(sec_agree), "not_finished_or_disagree": len(sec_bad),
          "sampled_larger": sum(1 for r in sec_cmp if r.get("sampled")),
          "gp_only_on_flint_undecided": [{"tag": r["tag"], "degree": r["degree"], "gp_rank_qq": r["gp_rank_qq"],
                                          "rank_p": r["flint_rank_p"], "rows": r["rows"], "cols": r["cols"]}
                                         for r in sec_extra],
          "passed": bool(sec_cmp) and len(sec_agree) == len(sec_cmp) and not sec_bad}
    g1_pass = bool(g1 and g1["passed"])
    g4_pass = bool(g4 and g4["passed"])
    p3 = {t: res.get(t) for t in P3_TAGS}
    passing_m1 = [r for r in rows if r["verdict"] == "pass" and r["m"] == 1]
    new_rays = ray_scope_tables(passing_m1)
    rest_pass = sum(1 for r in rest if r["verdict"] == "pass")
    sized = [(r["max_shape"], r["tag"]) for r in rows]
    big = max(sized, key=lambda x: x[0][0] * x[0][1], default=((0, 0), ""))
    long_rank = max(((d.get("seconds_qq") or 0, r["tag"], d["degree"]) for r in rows for d in r["degrees"]),
                    default=(0, "", 0))
    p1 = g1_pass and g2["passed"] and g3["passed"] and g4_pass
    p2a = rest_pass >= 55
    p2b = new_rays["become_char0_count"] >= 40
    p2b_closure = new_rays.get("become_char0_with_closures_count", 0) >= 40
    p3_fail = {t: (p3[t] or {}).get("verdict") for t in P3_TAGS}
    out = {"experiment": "EXP-004", "hits_total": len(hits), "hits_skipped": skipped, "hits_without_result": missing,
           "gates": {"G1": {"passed": g1_pass, "detail": g1}, "G2": g2, "G3": g3, "G4": {"passed": g4_pass, "detail": g4}},
           "counts_with_second_instrument_completing": {
               v: sum(1 for r in rows if r["verdict_two_instruments"] == v) for v in ("pass", "fail", "undecided")},
           "counts": {"all": count(rows), "known_ok": count(known), "rest": count(rest),
                      "by_exp001_qq_status": by_status},
           "predictions": {
               "P1": {"holds": p1, "G1": g1_pass, "G2": g2["passed"], "G3": g3["passed"], "G4": g4_pass},
               "P2": {"rest_hits": len(rest), "rest_pass": rest_pass, "threshold_rest": 55, "rest_holds": p2a,
                      "rays_only_gf32003": new_rays["only_gf32003_rays"],
                      "rays_become_char0_direct": new_rays["become_char0_count"], "threshold_rays": 40,
                      "rays_direct_holds": p2b, "rays_with_closures": new_rays.get("become_char0_with_closures_count"),
                      "rays_with_closures_holds": p2b_closure},
               "P3": {"verdicts": p3_fail,
                      "holds_both_fail": all(v == "fail" for v in p3_fail.values()),
                      "contradiction_a_hit_passes": any(v == "pass" for v in p3_fail.values())}},
           "p3_hits": p3, "rays": new_rays,
           "largest_matrix": {"rows": big[0][0], "cols": big[0][1], "tag": big[1]},
           "longest_rank_qq_seconds": {"seconds": long_rank[0], "tag": long_rank[1], "degree": long_rank[2]},
           "second_instrument": {"matrices": len(second), "finished": len(sec_ok), "compared": len(sec_cmp),
                                 "agree": len(sec_agree),
                                 "other": len(sec_bad), "sampled_larger": g3["sampled_larger"]},
           "hits": rows}
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "results.json").write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    (HERE / "results-summary.md").write_text(summary_text(out, rows), encoding="utf-8")
    log(f"table: results.json and results-summary.md written ({len(rows)} hits, {len(missing)} without a result)")
    return 0


def summary_text(o: dict, rows: list[dict]) -> str:
    g = o["gates"]
    c = o["counts"]
    p = o["predictions"]
    lines = ["# EXP-004 results summary", "",
             f"Generated by `run.py table` on {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')} from the logs in the data "
             "root. Numbers only; the verdict is written by the coordinating session.", "",
             "## Gates", ""]
    lines.append(f"- G1: {'passed' if g['G1']['passed'] else 'NOT PASSED'}"
                 + (f"; {g['G1']['detail']['matrices']} matrices of {g['G1']['detail']['hits']} hits, the ranks mod p "
                    "reproduce the pure Hilbert function in every degree" if g["G1"]["detail"] else "; not run"))
    lines.append(f"- G2: {'passed' if g['G2']['passed'] else 'NOT PASSED'}; {g['G2']['pass']} of {g['G2']['hits']} hits "
                 "with EXP-001 status ok pass the rank test")
    g3 = g["G3"]
    lines.append(f"- G3: {'passed' if g3['passed'] else 'NOT PASSED'}; the two instruments agree on {g3['agree']} of "
                 f"{g3['compared']} compared matrices ({g3['sampled_larger']} sampled from the larger ones); "
                 f"{g3['not_finished_or_disagree']} not finished or in disagreement")
    lines.append(f"- G4: {'passed' if g['G4']['passed'] else 'NOT PASSED'}"
                 + (f"; {g['G4']['detail']['summary']}" if g["G4"]["detail"] else "; not run"))
    lines += ["", "## Counts (130 hits; pass, fail, undecided)", "",
              "| set | hits | pass | fail | undecided |", "|---|---|---|---|---|"]
    al = c["all"]
    lines.append(f"| all verified hits | {len(rows)} | {al['pass']} | {al['fail']} | {al['undecided']} |")
    for st, v in c["by_exp001_qq_status"].items():
        lines.append(f"| EXP-001 QQ status {st} | {v['hits']} | {v['pass']} | {v['fail']} | {v['undecided']} |")
    r = c["rest"]
    lines.append(f"| the hits without a completed positive recheck | {sum(r.values())} | {r['pass']} | {r['fail']} | "
                 f"{r['undecided']} |")
    c2 = o["counts_with_second_instrument_completing"]
    lines += ["", "Matrices that python-flint left undecided at its time limit and PARI/GP completed are counted in the "
               f"next line: pass {c2['pass']}, fail {c2['fail']}, undecided {c2['undecided']}."]
    for r in rows:
        if r["degrees_decided_by_second_instrument"]:
            for d in r["degrees_decided_by_second_instrument"]:
                dd = next(x for x in o["gates"]["G3"]["gp_only_on_flint_undecided"]
                          if x["tag"] == r["tag"] and x["degree"] == d)
                lines.append(f"- {r['tag']} degree {d}: {dd['rows']}x{dd['cols']}, rank mod p {dd['rank_p']}, rank over "
                             f"QQ by PARI/GP {dd['gp_rank_qq']} (python-flint: undecided at the time limit).")
    lines += ["", "## Predictions", "",
              f"- P1 (G1 to G4 hold): {'holds' if p['P1']['holds'] else 'does not hold'}",
              f"- P2 (at least 55 of the {p['P2']['rest_hits']} hits without a completed positive recheck pass): "
              f"{p['P2']['rest_pass']} pass; {'holds' if p['P2']['rest_holds'] else 'does not hold'}",
              f"- P2 (at least 40 of the {p['P2']['rays_only_gf32003']} rays realized over GF(32003) only become "
              f"realized in characteristic 0): {p['P2']['rays_become_char0_direct']} by a passing hit at multiple 1 on "
              f"the ray itself; {p['P2']['rays_with_closures']} when duality and the census closures of EXP-001 "
              f"are applied; {'holds' if p['P2']['rays_direct_holds'] else 'does not hold'} on the direct count, "
              f"{'holds' if p['P2']['rays_with_closures_holds'] else 'does not hold'} with the closures",
              f"- P3 (the two named hits fail the rank test): verdicts {p['P3']['verdicts']}; "
              f"{'holds' if p['P3']['holds_both_fail'] else 'does not hold'}"
              + ("; A NAMED HIT PASSES THE RANK TEST (the contradiction of the hypothesis)"
                 if p["P3"]["contradiction_a_hit_passes"] else ""), "",
              "## P3 hits, rank by degree (degree: rows x cols, rank mod p, rank over QQ, Hilbert function)", ""]
    for t, rec in o["p3_hits"].items():
        lines.append(f"- {t}: {rec['verdict'] if rec else 'no result'}")
        if rec:
            for d in rec["degrees"]:
                lines.append(f"  - degree {d['degree']}: {d['rows']}x{d['cols']}, rank mod p {d['rank_p']}, rank QQ "
                             f"{d['rank_qq']}, Hilbert {d['hilbert']}")
    big, lr = o["largest_matrix"], o["longest_rank_qq_seconds"]
    s2 = o["second_instrument"]
    lines += ["", "## Sizes and times", "",
              f"- Largest matrix: {big['rows']} x {big['cols']} ({big['tag']}).",
              f"- Longest rank over QQ: {lr['seconds']} s ({lr['tag']}, degree {lr['degree']}).",
              f"- Second instrument: {s2['matrices']} matrices, {s2['finished']} finished, {s2['agree']} agree, "
              f"{s2['other']} not agreeing or not finished.", "",
              "## Rays", "",
              f"- Rays realized over GF(32003) only in EXP-001 at multiple 1: {o['rays']['only_gf32003_rays']}.",
              f"- Of these, realized in characteristic 0 by a passing hit at multiple 1 on the ray: "
              f"{o['rays']['become_char0_count']}."]
    for d in o["rays"]["become_char0_by_passing_hit_at_m1"]:
        lines.append(f"  - ({','.join(str(x) for x in d)})")
    cl = o["rays"].get("census_closure")
    if cl:
        lines.append(f"- With the census closures of EXP-001 (duality): characteristic 0 count {cl['char0_before']} "
                     f"before, {cl['char0_after']} after; {o['rays'].get('become_char0_with_closures_count')} of the "
                     "GF(32003)-only rays gain a characteristic 0 realization.")
        for d in o["rays"].get("become_char0_with_closures", []):
            lines.append(f"  - ({','.join(str(x) for x in d)})")
    elif "census_closure_error" in o["rays"]:
        lines.append(f"- Census closure not computed: {o['rays']['census_closure_error']}")
    if o["hits_skipped"]:
        lines.append(f"- Skipped hits: {len(o['hits_skipped'])}.")
    lines += ["", "## Hits not passing", ""]
    for r in rows:
        if r["verdict"] != "pass":
            lines.append(f"- {r['tag']}: {r['verdict']}; EXP-001 QQ status {r['exp001_qq']}; rank over QQ larger in "
                         f"degrees {r['degrees_rank_qq_larger']}; undecided degrees {r['degrees_undecided']}")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------------------------------------ main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["gates", "known", "rest", "second", "table"])
    ap.add_argument("--data-root", help="the data root (or the environment variable CAOS_RESEARCH_DATA)")
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--limit", type=float, default=QQ_LIMIT, help="seconds per rank over QQ")
    ap.add_argument("--gp-limit", type=float, default=GP_LIMIT, help="seconds per PARI/GP matrix")
    args = ap.parse_args()
    return {"gates": cmd_gates, "known": cmd_known, "rest": cmd_rest, "second": cmd_second,
            "table": cmd_table}[args.cmd](args)


if __name__ == "__main__":
    mp.freeze_support()
    sys.exit(main())
