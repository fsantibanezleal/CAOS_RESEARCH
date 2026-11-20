"""EXP-001 driver: the realizability table of the 220 pure rays over k[x,y,z]. CPU only, exact arithmetic.

Run from the repository root with the repo .venv. The data root is an argument or the environment variable
CAOS_RESEARCH_DATA (never a path in the code). Heavy outputs go to <data root>/boij-soderberg-realizability/EXP-001/.

    run.py stage0     census (census.py), G1 against Macaulay2, G2 against the dossier, G6 and G7
    run.py known      stage 1a: the known answers (G3), then the saved modules of their hits
    run.py soderberg  stage 1b: randomSocleModule(L, s/beta_0) on the 55 rays (0,a,a+1,d3), 3 seeds
    run.py search     stage 1c: both generators on every ray with low < up, resumable, at most 16 workers
    run.py verify     stage 1d: fresh Macaulay2, Singular mres on the saved presentation, QQ recheck
    run.py charflags  stage 1e: each hit's generator over GF(2), GF(3), GF(5), 5 seeds (no claim)
    run.py table      results.json, table.md, hits-manifest.json, results-summary.md

Macaulay2 1.22 and Singular 4.3.2 run in WSL. Each Macaulay2 process handles the cells of one ray, writes a
flushed JSON line per cell, and is killed from here (by the recorded pid) when one resolution exceeds the limit.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import queue
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import census as C  # noqa: E402

M2DIR = HERE / "m2"
ARTIFACTS = HERE / "artifacts"
DOSSIER = (HERE.parents[3] / "combinatorics" / "petersen-coloring" / "context" / "scouting-2026-09"
           / "2026-09-02-dossier-boij-soderberg-realizability.md")
SUBDIR = Path("boij-soderberg-realizability") / "EXP-001"
P_MAIN = 32003
SEEDS = (1, 2, 3)
TIME_LIMIT = 1200      # seconds per resolution (hypothesis, stage 1c)
QQ_LIMIT = 1800        # seconds per QQ recheck (hypothesis, stage 1d)
MAX_WORKERS = 16
MSEARCH_MAX = 4
GENERATORS = ("socle", "module")
VERIFIED_FIELDS = (P_MAIN, 101)
wsl_path = C.wsl_path
LOG_TO_ARTIFACT = False


# ------------------------------------------------------------------------------------------ small helpers

def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if LOG_TO_ARTIFACT:
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        with open(ARTIFACTS / "run.log", "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def ray_tag(d) -> str:
    return "-".join(str(x) for x in d)


def cell_key(d, m, gen, seed, p) -> str:
    return f"{ray_tag(d)}|{m}|{gen}|{seed}|{p}"


def append_jsonl(path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, sort_keys=True) + "\n")
        fh.flush()


def read_jsonl(path) -> list[dict]:
    path = Path(path)
    out = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def read_verify(base) -> dict:
    """Stage 1d records, the last line per hit winning (a QQ-only pass appends an updated record)."""
    out = {}
    for v in read_jsonl(Path(base) / "verify.jsonl"):
        out[(tuple(v["d"]), v["m"], v["gen"], v["seed"], v["p"])] = v
    return out


def load_cells(base) -> list[dict]:
    """Every finished cell (hit, miss, timeout, error) of every per-ray log."""
    out: list[dict] = []
    for f in sorted((Path(base) / "rays").glob("*.jsonl")):
        out += read_jsonl(f)
    return out


def load_done(base) -> set[str]:
    return {cell_key(c["d"], c["m"], c["gen"], c["seed"], c["p"]) for c in load_cells(base)}


def pending_cells(d, ms, gens, seeds, p, done) -> list[dict]:
    return [{"d": list(d), "m": m, "gen": g, "seed": s, "p": p}
            for m in ms for g in gens for s in seeds if cell_key(d, m, g, s, p) not in done]


def summarize_outcomes(cells) -> dict:
    out = {"hit": 0, "miss": 0, "timeout": 0, "error": 0}
    for c in cells:
        out[c["outcome"]] = out.get(c["outcome"], 0) + 1
    return out


def search_m_range(low, up) -> list[int]:
    """m from low_d to min(up_d - 1, 4); up None means nothing realized yet."""
    hi = MSEARCH_MAX if up is None else min(up - 1, MSEARCH_MAX)
    return list(range(low, hi + 1))


def singular_matches(text: str, d, beta, m: int) -> bool:
    """The Singular recheck: counts m*beta_i and every generator degree d_i, read from the resolution itself."""
    got = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 5 and parts[0] == "F":
            got[int(parts[1])] = tuple(int(x) for x in parts[2:])
    if sorted(got) != list(range(len(d))):
        return False
    return all(got[i] == (m * beta[i], d[i], d[i]) for i in range(len(d)))


def manifest_entry(path) -> dict:
    path = Path(path)
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return {"path": path.name, "sha256": h.hexdigest(), "bytes": path.stat().st_size}


def data_dir(args) -> Path:
    root = args.data_root or os.environ.get("CAOS_RESEARCH_DATA")
    if not root:
        raise SystemExit("data root missing: pass --data-root or set CAOS_RESEARCH_DATA")
    base = Path(root) / SUBDIR if not getattr(args, "raw_data_dir", False) else Path(root)
    for sub in ("rays", "hits", "work"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    return base


# ------------------------------------------------------------------------------------------ WSL processes

def kill_pid(pidfile: Path, proc) -> None:
    """Kill exactly the process this driver started (pid recorded by launch.sh), then its wsl.exe."""
    pid = ""
    for _ in range(20):
        try:
            pid = pidfile.read_text().strip()
        except OSError:
            pid = ""
        if pid:
            break
        time.sleep(0.25)
    if pid.isdigit():
        subprocess.run(["wsl", "-e", "kill", "-9", pid], capture_output=True, timeout=60)
    try:
        proc.kill()
    except OSError:
        pass


def launch(launcher: str, args: list[str], pidfile: Path):
    pidfile.parent.mkdir(parents=True, exist_ok=True)
    pidfile.unlink(missing_ok=True)
    cmd = ["wsl", "-e", "bash", wsl_path(str(M2DIR / launcher)), wsl_path(str(pidfile)), *args]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                            errors="replace", bufsize=1)


def run_wsl(launcher: str, args: list[str], timeout: float, pidfile: Path):
    """Run one WSL job to completion; (returncode or None on timeout, output, seconds)."""
    t0 = time.time()
    proc = launch(launcher, args, pidfile)
    try:
        out, _ = proc.communicate(timeout=timeout)
        return proc.returncode, out, time.time() - t0
    except subprocess.TimeoutExpired:
        kill_pid(pidfile, proc)
        try:
            out, _ = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            out = ""
        return None, out or "", time.time() - t0


# ------------------------------------------------------------------------------------------ hits to table

def hits_from_logs(base, include_flags: bool = False) -> list[dict]:
    """Realizations found by the search (first hit per ray, m, field), as entries for census.compute_tables."""
    base = Path(base)
    out, seen = [], set()
    for c in load_cells(base):
        if c["outcome"] != "hit" or (c["p"] not in VERIFIED_FIELDS and not include_flags):
            continue
        d, m, field = tuple(c["d"]), c["m"], f"GF({c['p']})"
        if (d, m, field) in seen:
            continue
        seen.add((d, m, field))
        out.append({"d": d, "m": m, "route": f"search:{c['gen']}", "field": field, "stage": c.get("stage", ""),
                    "evidence": f"{C.fmt(d)} m={m}: {c['gen']} generator, seed {c['seed']}, GF({c['p']}), "
                                f"module {', '.join(c.get('files', []))}"})
    for v in read_verify(base).values():
        if v.get("qq", {}).get("status") == "ok":
            d, m = tuple(v["d"]), v["m"]
            if (d, m, "QQ") not in seen:
                seen.add((d, m, "QQ"))
                out.append({"d": d, "m": m, "route": f"QQ recheck of search:{v['gen']}", "field": C.CHAR0,
                            "stage": "1d", "evidence": f"{C.fmt(d)} m={m}: {v['gen']} generator, seed {v['seed']}, "
                                                       f"matrix lifted from GF({v['p']}) to QQ, resolved over QQ"})
    return out


# ------------------------------------------------------------------------------------------ cell runner

class Ctx:
    def __init__(self, base: Path, stage: str, time_limit: float, workers: int, base_table: dict,
                 stop_after: int | None = None, stop_on_hit: bool = True):
        self.base, self.stage, self.time_limit = base, stage, time_limit
        self.workers = min(workers, MAX_WORKERS)
        self.base_table = base_table
        self.stop = threading.Event()
        self.stop_after, self.stop_on_hit = stop_after, stop_on_hit
        self.lock = threading.Lock()
        self.finished = 0
        self.g4: dict | None = None
        self.counts = {"hit": 0, "miss": 0, "timeout": 0, "error": 0}


def _record(ctx: Ctx, d, cell, obj: dict) -> None:
    rec = {"d": list(d), "m": cell["m"], "gen": cell["gen"], "seed": cell["seed"], "p": cell["p"],
           "outcome": obj["outcome"], "reason": obj.get("reason", ""), "totals": obj.get("totals", []),
           "seconds": obj.get("ms", 0) / 1000.0 if "seconds" not in obj else obj["seconds"],
           "files": obj.get("files", []), "stage": ctx.stage, "time": datetime.now().isoformat(timespec="seconds")}
    append_jsonl(ctx.base / "rays" / f"{ray_tag(d)}.jsonl", rec)
    with ctx.lock:
        ctx.counts[rec["outcome"]] = ctx.counts.get(rec["outcome"], 0) + 1
        ctx.finished += 1
        n = ctx.finished
    log(f"{C.fmt(d)} m={cell['m']} {cell['gen']} seed={cell['seed']} p={cell['p']} -> {rec['outcome']} "
        f"{rec['seconds']:.1f}s {rec['totals'] if rec['outcome'] != 'hit' else ''}".rstrip())
    if rec["outcome"] == "hit":
        viol = C.g4_violation(ctx.base_table, d, cell["m"])
        if viol:  # gate G4: a hit on an excluded point is a bug or a refuted proof; stop everything
            ctx.g4 = {"d": list(d), "m": cell["m"], "obstructions": viol, "cell": rec}
            (ctx.base / "G4_VIOLATION.json").write_text(json.dumps(ctx.g4, indent=1), encoding="utf-8")
            log(f"G4 VIOLATION {C.fmt(d)} m={cell['m']} excluded by {viol}: stopping every worker")
            ctx.stop.set()
    if ctx.stop_after is not None and n >= ctx.stop_after:
        ctx.stop.set()


def run_cells(ctx: Ctx, d, cells: list[dict]) -> None:
    """One Macaulay2 process per ray: restart after a timeout kill, record every cell, stop at a first hit."""
    tag = ray_tag(d)
    work, hits = ctx.base / "work", ctx.base / "hits"
    remaining = list(cells)
    noprogress = 0
    while remaining and not ctx.stop.is_set():
        cellsfile = work / f"{tag}.{ctx.stage}.cells.txt"
        cellsfile.write_text("".join(
            f"{','.join(str(x) for x in d)} {c['m']} {c['gen']} {c['seed']} {c['p']}\n" for c in remaining),
            encoding="utf-8")
        pidfile = work / f"{tag}.{ctx.stage}.pid"
        proc = launch("launch.sh", [wsl_path(str(M2DIR / "cells.m2")), wsl_path(str(cellsfile)),
                                    wsl_path(str(hits))], pidfile)
        q: queue.Queue = queue.Queue()

        def reader():
            for line in proc.stdout:
                q.put(line)
            q.put(None)

        threading.Thread(target=reader, daemon=True).start()
        cur, t_start, progressed, tail, hit_stop = None, 0.0, False, [], False
        while True:
            try:
                line = q.get(timeout=1.0)
            except queue.Empty:
                if ctx.stop.is_set():
                    kill_pid(pidfile, proc)
                    return
                if cur is not None and time.time() - t_start > ctx.time_limit:
                    kill_pid(pidfile, proc)
                    _record(ctx, d, cur, {"outcome": "timeout", "reason": f"resolution over {ctx.time_limit}s",
                                          "seconds": time.time() - t_start})
                    remaining = [c for c in remaining if c is not cur]
                    progressed = True
                    break
                continue
            if line is None:
                break
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                tail = (tail + [line.strip()])[-12:]
                continue
            ev = obj.get("event")
            if ev == "start":
                cur = next((c for c in remaining if (c["m"], c["gen"], c["seed"], c["p"])
                            == (obj["m"], obj["gen"], obj["seed"], obj["p"])), None)
                t_start = time.time()
            elif ev == "done" and cur is not None:
                _record(ctx, d, cur, obj)
                remaining = [c for c in remaining if c is not cur]
                progressed = True
                cur = None
                if obj["outcome"] == "hit" and ctx.stop_on_hit:
                    kill_pid(pidfile, proc)
                    remaining, hit_stop = [], True
                    break
                if ctx.stop.is_set():
                    kill_pid(pidfile, proc)
                    return
        try:
            proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            kill_pid(pidfile, proc)
        if hit_stop or not remaining:
            break
        if not progressed:  # the process died before finishing any cell: record the first cell as an error
            noprogress += 1
            if noprogress >= 2 and not ctx.stop.is_set():
                _record(ctx, d, remaining[0], {"outcome": "error", "reason": "process failed: " + " | ".join(tail)[-300:]})
                remaining = remaining[1:]
                noprogress = 0


def run_pool(ctx: Ctx, jobs) -> None:
    with cf.ThreadPoolExecutor(max_workers=ctx.workers) as ex:
        futs = [ex.submit(j) for j in jobs]
        for f in futs:
            f.result()


# ------------------------------------------------------------------------------------------ subcommands

def cmd_stage0(args) -> int:
    global LOG_TO_ARTIFACT
    LOG_TO_ARTIFACT = True
    data_dir(args)  # checks the data root argument and creates the folders
    table = C.compute_tables()
    counts = C.counts(table)
    g1 = C.check_m2()
    g2 = C.compare_appendix(C.parse_appendix(DOSSIER), table)
    g2["passed"] = not (g2["beta_mismatch"] or g2["es_mismatch"] or g2["parity_mismatch"] or g2["hf_mismatch"])
    g6 = C.gate_g6()
    g7 = C.gate_g7(g1.get("m2_pureCharFree_0_4_9_13"))
    out = {"counts": counts, "G1": g1, "G2": g2, "G6_census_part": g6, "G7": g7,
           "m2_file_sha256": "3ce45c08f73ea4c3fcc049f261d35c73b4b5a1afcf9c239a9806e2e0ed53b415",
           "time": datetime.now().isoformat(timespec="seconds")}
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "stage0.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    log(f"stage 0 counts: {json.dumps(counts)}")
    log(f"G1 {'passed' if g1['passed'] else 'FAILED'}: {g1['rays_compared']} rays compared with Macaulay2, "
        f"{len(g1['mismatches'])} mismatches; counts rays={g1['rays']} cyclic={g1['cyclic']} "
        f"parity={g1['parity_passing']}")
    log(f"G2 {'passed' if g2['passed'] else 'FAILED'}: columns beta/ES multiple/parity on {g2['rows']} rows, "
        f"mismatches beta={len(g2['beta_mismatch'])} es={len(g2['es_mismatch'])} parity={len(g2['parity_mismatch'])}; "
        f"status agrees on {g2['status_agree']}, differs on {len(g2['status_differences'])} (listed in stage0.json)")
    log(f"G6 census part {'passed' if g6['passed'] else 'FAILED'}: m=2 realization comes from stage 1a")
    log(f"G7: pureCharFree({g7['ray']}) = {g7['pureCharFree_python']} (Macaulay2 {g7['pureCharFree_macaulay2']}), "
        f"multiple {g7['multiple']}; the dossier printed example says {g7['dossier_printed_example']}")
    ok = g1["passed"] and g2["passed"] and g6["passed"] and g7["passed"]
    return 0 if ok else 1


def cmd_known(args) -> int:
    global LOG_TO_ARTIFACT
    LOG_TO_ARTIFACT = True
    base = data_dir(args)
    kfile = base / "known.jsonl"
    prev = read_jsonl(kfile)
    fields = [101, 32003, 0]
    todo = [p for p in fields if args.force or not any(r.get("event") == "finished" and r.get("p") == p for r in prev)]

    def one(p):
        rc, out, secs = run_wsl("launch.sh", [wsl_path(str(M2DIR / "known.m2")), str(p)], QQ_LIMIT,
                                base / "work" / f"known-{p}.pid")
        log(f"known p={p}: exit {rc}, {secs:.0f}s")
        for line in out.splitlines():
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("event") == "known":
                append_jsonl(kfile, obj)
            elif obj.get("event") == "finished":
                append_jsonl(kfile, {"event": "finished", "p": p, "seconds": secs})
        if rc is None:
            append_jsonl(kfile, {"event": "timeout", "p": p})

    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(one, todo))
    items = [r for r in read_jsonl(kfile) if r.get("event") == "known"]
    g3 = known_gate(items)
    log(f"G3 {'passed' if g3['passed'] else 'FAILED'} over ZZ/101 and GF(32003): {g3['summary']}")
    # stage 1a hits again through the cell runner, so that the modules are saved (stage 1d reads them)
    cells = {}
    for it in items:
        if it["p"] == P_MAIN and it["ok"] and it["cell"]:
            parts = it["cell"].split()
            d = tuple(int(x) for x in parts[0].split(","))
            cell = {"d": list(d), "m": int(parts[1]), "gen": parts[2], "seed": int(parts[3]), "p": P_MAIN}
            if cell not in cells.setdefault(d, []):
                cells[d].append(cell)
    ctx = Ctx(base, "1a", args.time_limit, args.workers, C.compute_tables(), stop_on_hit=False)
    done = load_done(base)
    jobs = []
    for d, cl in cells.items():
        todo_cells = [c for c in cl if cell_key(d, c["m"], c["gen"], c["seed"], c["p"]) not in done]
        if todo_cells:
            jobs.append(lambda d=d, tc=todo_cells: run_cells(ctx, d, tc))
    run_pool(ctx, jobs)
    return 0 if g3["passed"] and ctx.g4 is None else 1


def known_gate(items: list[dict]) -> dict:
    by_p: dict[int, list[dict]] = {}
    for it in items:
        by_p.setdefault(it["p"], []).append(it)
    summary = {str(p): f"{sum(1 for i in v if i['ok'])}/{len(v)}" for p, v in sorted(by_p.items())}
    need = [101, P_MAIN]
    passed = all(p in by_p and by_p[p] and all(i["ok"] for i in by_p[p]) for p in need)
    return {"passed": passed, "summary": summary, "failed": [i for i in items if not i["ok"]]}


def cmd_soderberg(args) -> int:
    global LOG_TO_ARTIFACT
    LOG_TO_ARTIFACT = True
    base = data_dir(args)
    ctx = Ctx(base, "1b", args.time_limit, args.workers, C.compute_tables(), stop_on_hit=False)
    done = load_done(base)
    jobs = []
    fam = [d for d in C.rays() if C.soderberg(d) is not None]
    fam.sort(key=lambda d: sum(C.primitive_point(d)) * (C.soderberg(d)["multiple"] or 1))
    for d in fam:
        s = C.soderberg(d)
        if not s["consistent"]:
            log(f"{C.fmt(d)}: Soderberg multiple not integral or socle type mismatch: {s}; not run")
            continue
        cells = pending_cells(d, [s["multiple"]], ["socle"], SEEDS, P_MAIN, done)
        if cells:
            jobs.append(lambda d=d, cells=cells: run_cells(ctx, d, cells))
    log(f"stage 1b: {len(fam)} rays in the family, {len(jobs)} with pending cells, {ctx.workers} workers")
    run_pool(ctx, jobs)
    log(f"stage 1b done: {ctx.counts}")
    return 0 if ctx.g4 is None else 4


def cmd_search(args) -> int:
    global LOG_TO_ARTIFACT
    LOG_TO_ARTIFACT = True
    base = data_dir(args)
    base_table = C.compute_tables()
    ctx = Ctx(base, args.stage, args.time_limit, args.workers, base_table, stop_after=args.stop_after,
              stop_on_hit=not args.no_stop_on_hit)
    if args.rays:
        rays = [tuple(int(x) for x in r.split(",")) for r in args.rays]
    else:
        rays = [d for d in C.rays() if base_table[d]["low"] < (base_table[d]["up"] or 99)]
    # cheap rays first: the smaller the Betti numbers, the sooner the closures prune the rest
    rays.sort(key=lambda d: (sum(C.primitive_point(d)), d))
    if args.smoke:
        pass
    info = {"pid": os.getpid(), "command": " ".join(sys.argv), "log_dir": str(base / "rays"),
            "started": datetime.now().isoformat(timespec="seconds"), "rays_queued": len(rays),
            "follow": f"python {HERE.name}/run.py table --data-root <root>  (or tail the per-ray logs in log_dir)"}
    if not args.smoke:
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        (ARTIFACTS / "background.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    log(f"search: {len(rays)} rays queued, {ctx.workers} workers, limit {args.time_limit}s per resolution, pid {os.getpid()}")

    def job(d):
        if ctx.stop.is_set():
            return
        if args.force_m:
            ms = list(args.force_m)
        else:
            table = C.compute_tables(extra_realized=hits_from_logs(base))
            ms = search_m_range(table[d]["low"], table[d]["up"])
        cells = pending_cells(d, ms, GENERATORS, SEEDS, P_MAIN, load_done(base))
        if cells:
            run_cells(ctx, d, cells)

    run_pool(ctx, [lambda d=d: job(d) for d in rays])
    log(f"search finished or stopped: {ctx.counts}, G4 violation: {ctx.g4}")
    return 0 if ctx.g4 is None else 4


SING_CHECK = r"""
int nr=nrows(P);
intvec w=0;
int i; int j; int k;
for(i=2;i<=nr;i++){ w[i]=0; }
attrib(M,"isHomog",w);
resolution re=mres(M,0);
proc coldeg(module N, intvec v, int k)
{
  int j;
  for(j=1;j<=nrows(N);j++){ if(N[k][j]!=0){ return(deg(N[k][j])+v[j]); } }
  return(-1);
}
print("F 0 "+string(nr)+" 0 0");
intvec cur=w; intvec nxt; int mn; int mx; int dg;
for(i=1;i<=size(re);i++)
{
  nxt=0; mn=100000; mx=-100000;
  for(k=1;k<=ncols(re[i]);k++){ dg=coldeg(re[i],cur,k); nxt[k]=dg; if(dg<mn){mn=dg;} if(dg>mx){mx=dg;} }
  print("F "+string(i)+" "+string(ncols(re[i]))+" "+string(mn)+" "+string(mx));
  cur=nxt;
}
quit;
"""


def hit_tag(c: dict) -> str:
    return f"{ray_tag(c['d'])}_m{c['m']}_{c['gen']}_s{c['seed']}_p{c['p']}"


def cmd_verify(args) -> int:
    global LOG_TO_ARTIFACT
    LOG_TO_ARTIFACT = True
    base = data_dir(args)
    vfile = base / "verify.jsonl"
    recs = read_verify(base)
    hits, seen = [], set()
    for c in load_cells(base):
        if c["outcome"] != "hit" or c["p"] not in VERIFIED_FIELDS or not c.get("files"):
            continue
        key = (tuple(c["d"]), c["m"])
        if key in seen and not args.all:
            continue
        seen.add(key)
        rec = recs.get((tuple(c["d"]), c["m"], c["gen"], c["seed"], c["p"]))
        if args.qq_only:
            if rec is not None and rec["qq"]["status"] == "not run":
                hits.append((c, rec))
        elif rec is None:
            hits.append((c, None))
    if args.rays:  # targeted rechecks: only the named rays
        wanted = {tuple(int(x) for x in r.split(",")) for r in args.rays}
        hits = [t for t in hits if tuple(t[0]["d"]) in wanted]
    hits.sort(key=lambda t: sum(C.primitive_point(tuple(t[0]["d"]))) * t[0]["m"])
    log(f"stage 1d: {len(hits)} hits to verify ({'QQ only' if args.qq_only else 'fresh and Singular'}"
        f"{'' if args.qq_only or not args.skip_qq else ', QQ skipped'}; {'all hits' if args.all else 'one per (ray, m)'})")

    def qq_check(c, tag, hf):
        rc, out, secs = run_wsl("launch.sh", [wsl_path(str(M2DIR / "recheck.m2")), "qq", wsl_path(str(hf))],
                                QQ_LIMIT, base / "work" / f"{tag}.v3.pid")
        status = "timeout" if rc is None else "fail"
        for line in out.splitlines():
            if line.startswith("{") and '"recheck"' in line:
                status = "ok" if json.loads(line)["ok"] else "fail"
        return {"status": status, "seconds": round(secs, 1)}

    def one(item):
        c, rec = item
        d, m = tuple(c["d"]), c["m"]
        tag = hit_tag(c)
        hf = base / "hits" / f"{tag}.hit.m2"
        if args.qq_only:
            res = dict(rec)
            res["qq"] = qq_check(c, tag, hf)
        else:
            res = {"d": list(d), "m": m, "gen": c["gen"], "seed": c["seed"], "p": c["p"], "tag": tag}
            rc, out, secs = run_wsl("launch.sh", [wsl_path(str(M2DIR / "recheck.m2")), "fresh", wsl_path(str(hf))],
                                    1800, base / "work" / f"{tag}.v1.pid")
            ok = False
            for line in out.splitlines():
                if line.startswith("{") and '"recheck"' in line:
                    ok = json.loads(line)["ok"]
            res["fresh_m2"] = {"ok": ok, "seconds": round(secs, 1), "exit": rc}
            sing = base / "work" / f"{tag}.verify.sing"
            sing.write_text((base / "hits" / f"{tag}.sing").read_text(encoding="utf-8") + SING_CHECK, encoding="utf-8")
            rc, out, secs = run_wsl("launch_singular.sh", [wsl_path(str(sing))], 3600, base / "work" / f"{tag}.v2.pid")
            sok = rc is not None and singular_matches(out, d, C.primitive_point(d), m)
            res["singular"] = {"ok": bool(sok), "seconds": round(secs, 1), "exit": rc, "output": out.strip()[-200:]}
            res["qq"] = {"status": "not run", "seconds": 0} if args.skip_qq else qq_check(c, tag, hf)
        append_jsonl(vfile, res)
        log(f"verify {C.fmt(d)} m={m} {c['gen']}: fresh={res['fresh_m2']['ok']} singular={res['singular']['ok']} "
            f"qq={res['qq']['status']} ({res['fresh_m2']['seconds']}+{res['singular']['seconds']}+{res['qq']['seconds']}s)")

    with cf.ThreadPoolExecutor(max_workers=min(args.workers, MAX_WORKERS)) as ex:
        list(ex.map(one, hits))
    return 0


def cmd_charflags(args) -> int:
    global LOG_TO_ARTIFACT
    LOG_TO_ARTIFACT = True
    base = data_dir(args)
    ctx = Ctx(base, "1e", args.time_limit, args.workers, C.compute_tables(), stop_on_hit=False)
    done = load_done(base)
    jobs, seen = [], set()
    for c in load_cells(base):
        if c["outcome"] != "hit" or c["p"] != P_MAIN:
            continue
        key = (tuple(c["d"]), c["m"], c["gen"])
        if key in seen:
            continue
        seen.add(key)
        d = tuple(c["d"])
        cells = []
        for p in (2, 3, 5):
            cells += pending_cells(d, [c["m"]], [c["gen"]], range(1, 6), p, done)
        if cells:
            jobs.append(lambda d=d, cells=cells: run_cells(ctx, d, cells))
    log(f"stage 1e: {len(jobs)} generators to rerun over GF(2), GF(3), GF(5), 5 seeds each (flags, no claim)")
    run_pool(ctx, jobs)
    return 0


# ------------------------------------------------------------------------------------------ table and summary

def staged_counts(base) -> dict:
    hits = hits_from_logs(base)
    out = {}
    for label, stages in (("stage 0", ()), ("after 1a", ("1a",)), ("after 1b", ("1a", "1b")),
                          ("after 1c", ("1a", "1b", "1c")), ("after 1d (QQ rechecks)", ("1a", "1b", "1c", "1d"))):
        out[label] = C.counts(C.compute_tables(extra_realized=[h for h in hits if h["stage"] in stages]))
    return out


def cmd_table(args) -> int:
    global LOG_TO_ARTIFACT
    LOG_TO_ARTIFACT = True
    base = data_dir(args)
    hits = hits_from_logs(base)
    base_table = C.compute_tables()
    table = C.compute_tables(extra_realized=hits)
    cells = load_cells(base)
    stage0 = json.loads((ARTIFACTS / "stage0.json").read_text(encoding="utf-8")) if (ARTIFACTS / "stage0.json").exists() else {}
    known = [r for r in read_jsonl(base / "known.jsonl") if r.get("event") == "known"]
    g3 = known_gate(known) if known else {"passed": None, "summary": "stage 1a not run"}
    known_ok = {p: all(i["ok"] for i in known if i["p"] == p) for p in (101, P_MAIN, 0)} if known else {}
    g6 = C.gate_g6({"(0,4,9,10)": any(e["m"] == 2 for e in hits if tuple(e["d"]) == (0, 4, 9, 10))
                    and bool(known and known_ok.get(P_MAIN)),
                    "(0,1,6,10)": 2 in table[(0, 1, 6, 10)]["realized"] and bool(known and known_ok.get(P_MAIN))})
    viol = [{"d": list(h["d"]), "m": h["m"], "ids": C.g4_violation(base_table, h["d"], h["m"])}
            for h in hits if C.g4_violation(base_table, h["d"], h["m"])]
    ver = list(read_verify(base).values())
    g5 = {"verified": len(ver), "fresh_m2_failed": [v["tag"] for v in ver if not v["fresh_m2"]["ok"]],
          "singular_failed": [v["tag"] for v in ver if not v["singular"]["ok"]],
          "qq_ok": sum(1 for v in ver if v["qq"]["status"] == "ok"),
          "qq_failed": [v["tag"] for v in ver if v["qq"]["status"] == "fail"],
          "qq_timeout": [v["tag"] for v in ver if v["qq"]["status"] == "timeout"],
          "qq_not_run": sum(1 for v in ver if v["qq"]["status"] == "not run")}
    g5["passed"] = bool(ver) and not g5["fresh_m2_failed"] and not g5["singular_failed"]
    gates = {"G1": stage0.get("G1", {}), "G2": stage0.get("G2", {}), "G3": g3, "G4": {"violations": viol,
             "passed": not viol and not (base / "G4_VIOLATION.json").exists()},
             "G5": g5, "G6": g6, "G7": stage0.get("G7", {})}
    search = {cell_key(c["d"], c["m"], c["gen"], c["seed"], c["p"]): {"outcome": c["outcome"],
              "seconds": c["seconds"], "stage": c.get("stage", ""), "reason": c.get("reason", "")} for c in cells}
    rays_out = []
    for d in C.rays():
        rec = dict(table[d])
        rec["excluded"] = {str(k): v for k, v in rec["excluded"].items()}
        rec["realized"] = {str(k): v for k, v in rec["realized"].items()}
        rays_out.append(rec)
    counts = C.counts(table)
    results = {"rays": rays_out, "gates": gates, "search": search, "counts": counts,
               "counts_by_stage": staged_counts(base), "outcomes": summarize_outcomes(cells)}
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS / "results.json").write_text(json.dumps(results, indent=1, default=str), encoding="utf-8")
    write_table_md(table)
    manifest = write_manifest(base, cells)
    write_summary(base, table, counts, results, manifest, cells, ver)
    log(f"table written: counts {json.dumps(counts)}")
    return 0


def route_of_primitive(rec) -> str:
    entries = rec["realized"].get(1)
    if not entries:
        return ""
    e = entries[0]
    return f"{e['route']} ({e['field']})"


def write_table_md(table: dict) -> None:
    lines = ["| d | beta | parity | low | up | primitive point | route and field | c_d |", "|---|---|---|---|---|---|---|---|"]
    for d in C.rays():
        r = table[d]
        route = route_of_primitive(r) if r["status_primitive"] == "realized" else (
            ",".join(r["excluded"][1]) if r["status_primitive"] == "excluded" else "")
        cd = str(r["low"]) if r["up"] is not None and r["low"] == r["up"] else ""
        lines.append(f"| {C.fmt(d)} | ({','.join(map(str, r['beta']))}) | {r['parity']} | {r['low']} | "
                     f"{r['up'] if r['up'] is not None else ''} | {r['status_primitive']} | {route} | {cd} |")
    (ARTIFACTS / "table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(base: Path, cells: list[dict]) -> dict:
    entries = []
    for c in cells:
        if c["outcome"] == "hit" and c.get("files"):
            entries.append({"d": c["d"], "m": c["m"], "gen": c["gen"], "seed": c["seed"], "p": c["p"],
                            "stage": c.get("stage", ""),
                            "files": [dict(manifest_entry(base / "hits" / f), path=f"hits/{f}") for f in c["files"]
                                      if (base / "hits" / f).exists()]})
    man = {"data_root_subdir": str(SUBDIR).replace("\\", "/"), "hits": entries,
           "known_jsonl": manifest_entry(base / "known.jsonl") if (base / "known.jsonl").exists() else None,
           "verify_jsonl": manifest_entry(base / "verify.jsonl") if (base / "verify.jsonl").exists() else None,
           "macaulay2_package_sha256": "3ce45c08f73ea4c3fcc049f261d35c73b4b5a1afcf9c239a9806e2e0ed53b415"}
    (ARTIFACTS / "hits-manifest.json").write_text(json.dumps(man, indent=1), encoding="utf-8")
    return man


def write_summary(base, table, counts, results, manifest, cells, ver) -> None:
    gates = results["gates"]
    cb = results["counts_by_stage"]
    L = ["# EXP-001 results summary", "",
         f"Generated by `run.py table` on {datetime.now().isoformat(timespec='seconds')} from the logs in the data "
         "root. Numbers only; the verdict is written by the coordinating session.", "", "## Gates", ""]
    g1, g2 = gates["G1"], gates["G2"]
    L += [f"- G1: {'passed' if g1.get('passed') else 'NOT PASSED'}; {g1.get('rays_compared')} rays compared with "
          f"Macaulay2, {len(g1.get('mismatches', []))} mismatches; rays {g1.get('rays')}, B0 = 1: {g1.get('cyclic')}, "
          f"parity passing: {g1.get('parity_passing')}.",
          f"- G2: columns beta, Eisenbud-Schreyer multiple and parity (and the U(H) Hilbert flag) reproduced on "
          f"{g2.get('rows')} rows: {'passed' if g2.get('passed') else 'NOT PASSED'}; status agrees on "
          f"{g2.get('status_agree')} rows and differs on {len(g2.get('status_differences', []))}.",
          f"- G3: {'passed' if gates['G3'].get('passed') else 'NOT PASSED'} ({gates['G3'].get('summary')}; per field "
          "ok/total, fields 101, 32003, 0 = QQ).",
          f"- G4: {'passed (no hit on an excluded point)' if gates['G4']['passed'] else 'VIOLATED ' + json.dumps(gates['G4']['violations'])}.",
          f"- G5: {g5_line(gates['G5'])}",
          f"- G6: {'passed' if gates['G6']['passed'] else 'NOT PASSED'}: " + json.dumps(gates['G6']['details']),
          f"- G7: pureCharFree({gates['G7'].get('ray')}) = {gates['G7'].get('pureCharFree_python')} in Python and "
          f"{gates['G7'].get('pureCharFree_macaulay2')} in Macaulay2, multiple {gates['G7'].get('multiple')}; the dossier "
          f"printed example says {gates['G7'].get('dossier_printed_example')}.", "",
          "## Counts after each stage (over S; primitive point = multiple 1)", "",
          "| stage | realized (some field) | realized over every field or every infinite field | "
          "realized in characteristic 0 | excluded | open | rays with c_d determined |",
          "|---|---|---|---|---|---|---|"]
    for label, c in cb.items():
        L.append(f"| {label} | {c['primitive_realized']} | {c['primitive_realized_any_or_infinite_field']} | "
                 f"{c['primitive_realized_char0']} | {c['primitive_excluded']} | {c['primitive_open']} | "
                 f"{c['c_determined']} |")
    L += ["", "Realized at stage 0 splits into 52 realized over every field (or every infinite field) and 26 realized "
          "only in characteristic 0, by the pureWeyman formula of Eisenbud-Floystad-Weyman (the dossier's Appendix A "
          "counts only the Eisenbud-Schreyer formula and the classical constructions).", "",
          "## Outcomes of the search cells", "", f"{json.dumps(results['outcomes'])} over {len(cells)} finished cells "
          "(a timeout is not a miss).", "", "## Hits and field scope", "",
          "First hit per (ray, m); every hit is in the per-ray logs and `hits-manifest.json`.", "",
          "| d | m | generator | seed | field | stage | fresh M2 | Singular | QQ recheck |",
          "|---|---|---|---|---|---|---|---|---|"]
    qq = {(tuple(v["d"]), v["m"]): v for v in ver}
    shown = set()
    for c in sorted(cells, key=lambda c: (c["d"][1:], c["m"])):
        if c["outcome"] == "hit" and c["p"] in VERIFIED_FIELDS and (tuple(c["d"]), c["m"]) not in shown:
            shown.add((tuple(c["d"]), c["m"]))
            v = qq.get((tuple(c["d"]), c["m"]))
            L.append(f"| {C.fmt(c['d'])} | {c['m']} | {c['gen']} | {c['seed']} | GF({c['p']}) | {c.get('stage', '')} | "
                     f"{('ok' if v['fresh_m2']['ok'] else 'FAILED') if v else 'not run'} | "
                     f"{('ok' if v['singular']['ok'] else 'FAILED') if v else 'not run'} | "
                     f"{v['qq']['status'] if v else 'not run'} |")
    L += ["", "## Stage 1b (Soderberg family)", ""]
    fam = [d for d in C.rays() if C.soderberg(d) is not None]
    pure = 0
    rows = []
    for d in fam:
        s = C.soderberg(d)
        got = [c for c in cells if tuple(c["d"]) == d and c["m"] == s["multiple"] and c["gen"] == "socle"
               and c["p"] == P_MAIN and c.get("stage") in ("1b", "1a", "1c")]
        hits = sum(1 for c in got if c["outcome"] == "hit")
        if len(got) >= 3 and hits == len(got):
            pure += 1
        rows.append((d, s, hits, len(got)))
    L += [f"Rays pure on every finished seed at m = s/beta_0: {pure} of {len(fam)}.", "",
          "| d | m = s/beta_0 | hits / cells run |", "|---|---|---|"]
    for d, s, h, n in rows:
        L.append(f"| {C.fmt(d)} | {s['multiple']} | {h} / {n} |")
    # predictions
    base0 = C.compute_tables()
    sub9_open = [d for d in C.rays() if d[3] <= 9 and table[d]["status_primitive"] == "open"]
    L += ["", "## Comparison with the predictions of hypothesis.md", ""]
    p1 = cb["stage 0"]
    L += [f"- P1: G1, G2, G6 {'hold' if g1.get('passed') and g2.get('passed') and gates['G6']['passed'] else 'do not all hold'}. "
          f"Stage 0 primitive points realized: {p1['primitive_realized']} (predicted 52 to 56; "
          f"{p1['primitive_realized_any_or_infinite_field']} over every field or every infinite field, "
          f"{p1['primitive_realized_char0_or_one_prime_only']} only in characteristic 0 by the EFW formula); "
          f"excluded at m = 1: {p1['primitive_excluded']} (predicted exactly 12); points with m >= 2 excluded by "
          f"O1 to O6: {sum(1 for r in table.values() for m in r['excluded'] if m >= 2)} (predicted none).",
          f"- P2: Soderberg family pure on all 55 rays at m = s/beta_0 over GF(32003): {pure} of {len(fam)} so far.",
          f"- P3: primitive points realized by search (stages 1a to 1c) among rays open after stage 0: "
          f"{sum(1 for d in C.rays() if base0[d]['status_primitive'] == 'open' and table[d]['status_primitive'] == 'realized')}; (0,3,4,8) primitive: "
          f"{table[(0, 3, 4, 8)]['status_primitive']}; rays with c_d determined: {counts['c_determined']} of 220 "
          "(predicted at least 100 in all).",
          f"- P4: hits persisting over QQ: {sum(1 for v in ver if v['qq']['status'] == 'ok')} of {len(ver)} verified "
          f"({sum(1 for v in ver if v['qq']['status'] == 'timeout')} timeouts, "
          f"{sum(1 for v in ver if v['qq']['status'] == 'fail')} failures).",
          f"- P5: rays with d3 <= 9 whose primitive point is still open: {len(sub9_open)}, of which parity-failing "
          f"{sum(1 for d in sub9_open if table[d]['parity'] != 0)}; parity-failing rays with d3 <= 9 with the primitive "
          f"point realized: {sum(1 for d in C.rays() if d[3] <= 9 and table[d]['parity'] != 0 and table[d]['status_primitive'] == 'realized')} "
          f"of {sum(1 for d in C.rays() if d[3] <= 9 and table[d]['parity'] != 0)}.", "",
          "## Rays with d3 <= 9 whose primitive point is still open", "", "| d | beta | parity p(-1) | low | up |", "|---|---|---|---|---|"]
    for d in sub9_open:
        r = table[d]
        L.append(f"| {C.fmt(d)} | ({','.join(map(str, r['beta']))}) | {r['parity']} | {r['low']} | {r['up']} |")
    bg = ARTIFACTS / "background.json"
    L += ["", "## State of the background search (stage 1c)", ""]
    L += [("```\n" + bg.read_text(encoding="utf-8") + "\n```") if bg.exists() else "not started"]
    pend = [d for d in C.rays() if table[d]["low"] < (table[d]["up"] or 99)]
    L += ["", f"Rays with low < up now: {len(pend)}. Cells finished: {len(cells)}. Data root logs: "
          "`rays/<ray>.jsonl` (one JSON line per finished cell); rerunning `run.py search` skips them.", ""]
    notes = ARTIFACTS / "summary-notes.md"
    if notes.exists():
        L += ["## Notes and deviations", "", notes.read_text(encoding="utf-8")]
    (HERE / "results-summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def g5_line(g5) -> str:
    return (f"{'passed' if g5['passed'] else 'NOT PASSED'}: {g5['verified']} hits verified in a fresh Macaulay2 "
            f"process and in Singular (failures: fresh {len(g5['fresh_m2_failed'])}, Singular {len(g5['singular_failed'])}); "
            f"QQ ok {g5['qq_ok']}, QQ failed {g5['qq_failed']}, QQ timeouts {g5['qq_timeout']}, QQ not run {g5['qq_not_run']}.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("stage0", cmd_stage0), ("known", cmd_known), ("soderberg", cmd_soderberg),
                     ("search", cmd_search), ("verify", cmd_verify), ("charflags", cmd_charflags),
                     ("table", cmd_table)):
        sp = sub.add_parser(name)
        sp.add_argument("--data-root", default=None, help="data root (default: env CAOS_RESEARCH_DATA)")
        sp.add_argument("--workers", type=int, default=MAX_WORKERS)
        sp.add_argument("--time-limit", type=float, default=TIME_LIMIT)
        sp.add_argument("--force", action="store_true")
        sp.add_argument("--all", action="store_true", help="verify: every hit, not one per (ray, m)")
        sp.add_argument("--rays", nargs="*", help="search: rays as 0,d1,d2,d3 (default: every ray with low < up)")
        sp.add_argument("--force-m", nargs="*", type=int, help="search: explicit multiples (smoke tests)")
        sp.add_argument("--stage", default="1c")
        sp.add_argument("--stop-after", type=int, default=None, help="search: stop after N finished cells (smoke)")
        sp.add_argument("--no-stop-on-hit", action="store_true")
        sp.add_argument("--smoke", action="store_true")
        sp.add_argument("--skip-qq", action="store_true", help="verify: fresh Macaulay2 and Singular only")
        sp.add_argument("--qq-only", action="store_true", help="verify: only the QQ recheck of verified hits")
        sp.set_defaults(fn=fn)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
