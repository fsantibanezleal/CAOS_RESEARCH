# EXP-146: Case 1 of JCB-103 by single-prime resultant-chain certificates with proven degree bounds.
# CPU only; exact integer arithmetic (python-flint, Hungarian on int64); second implementation in Singular 4.3.2 (WSL).
# See hypothesis.md (frozen). Run from the repository root:
#   .venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-146-case1-chain-certificate/run.py
#
# Gates in order (stop on failure): G0 inputs, G1 ring maps, G2 random bound soundness, G3 degree-drop formula,
# G4 controls. Then both branch trees at (p1, r1) (G2 on the real system and G5 are checked inside every node),
# the replay of every leaf at (p2, r2), and the Singular check (M9).
# Writes artifacts/results.json, slp-plus.json, slp-minus.json, singular-check.txt, run-log.txt; exact levels go to
# the data root. Exit 0 on CONFIRMED, 1 on a failed gate or check, 2 on UNKNOWN (a node failed or timed out), 3 on a
# missing input.
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import chaincert as cc  # noqa: E402
import gates  # noqa: E402
import singular_eval as se  # noqa: E402

ART = HERE / "artifacts"
DATA = Path("E:/_Datos/caos-research/jacobian-conjecture/exp146")
TEMP = Path("D:/_Temp/jc-exp146-2026-11-15")
BUDGET_SECONDS = 6 * 3600
ORDER = ["q5", "q3", "q4", "q2", "q0"]
LOG = []


def log(msg=""):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG.append(line)


def load_branch(tag):
    d = json.loads(gates.BRANCH[tag].read_text())
    ring = cc.NodeRing(ORDER)
    terms, ins = {}, []
    for frm, eq in zip(d["from"], d["eqs"]):
        mid = f"E{frm}"
        tl = [([m[d["names"].index(v)] for v in ORDER], cs) for m, cs in eq]
        terms[mid] = tl
        ins.append((mid, ring.from_vectors(tl)))
    return ring, ins, terms


def write(path, obj):
    path.write_text(json.dumps(obj, indent=1, default=str), encoding="utf-8")


def finish(results, verdict, code):
    results["verdict"] = verdict
    ART.mkdir(exist_ok=True)
    write(ART / "results.json", results)
    (ART / "run-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    log(f"VERDICT {verdict}")
    return code


def main():
    t_start = time.time()
    deadline = t_start + BUDGET_SECONDS
    ART.mkdir(exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    TEMP.mkdir(parents=True, exist_ok=True)
    results = {"experiment": "EXP-146", "gates": {}, "branches": {}, "replay": {}, "singular": {}}
    prime1 = cc.Prime(gates.P1, gates.R1)
    prime2 = gates.second_prime()
    results["primes"] = {"p1": prime1.p, "r1": prime1.r, "p2": prime2.p, "r2": prime2.r}
    log(f"(p1, r1) = ({prime1.p}, {prime1.r}); (p2, r2) = ({prime2.p}, {prime2.r})")

    # ---- G0 ----
    g0 = gates.g0_inputs(TEMP)
    results["gates"]["G0"] = g0
    log(f"G0 inputs: {'PASS' if g0['pass'] else 'FAIL'} {g0}")
    if not g0["pass"]:
        return finish(results, "STOPPED at G0", 3 if "reason" in g0 else 1)
    # ---- G1 ----
    g1 = gates.g1_ring_maps(prime2)
    results["gates"]["G1"] = g1
    log(f"G1 ring maps: {'PASS' if g1['pass'] else 'FAIL'}")
    if not g1["pass"]:
        return finish(results, "STOPPED at G1", 1)
    # ---- G2 random ----
    t = time.time()
    g2 = gates.g2_random(2000)
    results["gates"]["G2_random"] = g2
    log(f"G2 random pairs: {'PASS' if g2['pass'] else 'FAIL'} {g2} ({time.time() - t:.0f} s)")
    if not g2["pass"]:
        return finish(results, "STOPPED at G2", 1)
    # ---- G3 ----
    t = time.time()
    g3 = gates.g3_degree_drop(500, prime1)
    results["gates"]["G3"] = g3
    log(f"G3 degree-drop formula: {'PASS' if g3['pass'] else 'FAIL'} {g3} ({time.time() - t:.0f} s)")
    if not g3["pass"]:
        return finish(results, "STOPPED at G3", 1)
    # ---- G4 ----
    t = time.time()
    g4 = gates.g4_controls(prime1, gates.BRANCH["plus"], node_seconds=600, removal_cases=range(6), log=log)
    results["gates"]["G4"] = g4
    log(f"G4 controls: {'PASS' if g4['pass'] else 'FAIL'} {g4} ({time.time() - t:.0f} s)")
    if not g4["pass"]:
        return finish(results, "STOPPED at G4 (a certificate on a nonempty system is a bug)", 1)

    # ---- production ----
    states, allrecs = {}, {}
    for tag in ("plus", "minus"):
        ring, ins, terms = load_branch(tag)
        t = time.time()
        log(f"branch {tag}: tree at (p1, r1)")
        ok, st = cc.solve_tree(ORDER, ins, prime1, max_depth=4, node_seconds=1800, deadline=deadline,
                               log=log, tag="t")
        states[tag] = (st, terms)
        allrecs[tag] = st.records
        results["branches"][tag] = {"certified": bool(ok), "seconds": round(time.time() - t, 1),
                                    "nodes": st.records}
        log(f"branch {tag}: {'CERTIFIED' if ok else 'NOT certified'} in {time.time() - t:.0f} s")
        # exact levels to the data root
        dump = {nid: {mid: {str(k): str(v) for k, v in ex.to_dict().items()} for mid, ex in nd["exact"].items()}
                for nid, nd in st.nodes.items()}
        write(DATA / f"exact-levels-{tag}.json", dump)
    g2real = sum(r.get("gate", {}).get("g2_real_checked", 0) for t_ in allrecs.values() for r in t_)
    g2viol = sum(r.get("gate", {}).get("g2_real_violations", 0) for t_ in allrecs.values() for r in t_)
    g5chk = sum(r.get("gate", {}).get("g5_checked", 0) for t_ in allrecs.values() for r in t_)
    g5mis = sum(r.get("gate", {}).get("g5_mismatches", 0) for t_ in allrecs.values() for r in t_)
    results["gates"]["G2_real_system"] = {"exact_levels_checked": g2real, "violations": g2viol, "pass": g2viol == 0}
    results["gates"]["G5"] = {"exact_levels_checked": g5chk, "mismatches": g5mis, "pass": g5mis == 0 and g5chk > 0}
    log(f"G2 real system: {g2real} exact levels, {g2viol} violations; G5: {g5chk} exact levels, {g5mis} mismatches")
    unknown = [(tag, r["id"], r.get("reason")) for tag, rs in allrecs.items() for r in rs if r["status"] == "unknown"]
    results["unknown_nodes"] = unknown
    all_cert = all(results["branches"][t]["certified"] for t in ("plus", "minus"))

    # ---- replay at (p2, r2) ----
    replay_ok = True
    for tag, (st, terms) in states.items():
        results["replay"][tag] = {}
        for r in st.records:
            if r["status"] != "certified":
                continue
            rp = cc.replay_leaf(st, r, prime2)
            results["replay"][tag][r["id"]] = rp
            replay_ok = replay_ok and rp["certified"] and not rp["problems"]
            log(f"replay {tag} {r['id']} at p2: certified={rp['certified']} problems={rp['problems']}")
    results["gates"]["replay_p2"] = {"pass": bool(replay_ok)}

    # ---- Singular ----
    sing_ok = True
    sing_txt = []
    for tag, (st, terms) in states.items():
        script = se.build_script(st.records, terms, ORDER, prime1)
        t = time.time()
        log(f"Singular check {tag}: running")
        rc, out, err = se.run_singular(script, TEMP, name=f"check-{tag}")
        cmp_ = se.compare(st.records, out, prime1)
        cmp_["returncode"] = rc
        cmp_["seconds"] = round(time.time() - t, 1)
        cmp_["stderr_tail"] = err[-500:]
        results["singular"][tag] = cmp_
        sing_ok = sing_ok and cmp_["pass"] and rc == 0
        sing_txt.append(f"== branch {tag}: returncode {rc}, seconds {cmp_['seconds']}\n"
                        f"digests compared {cmp_['digests_compared']}, mismatches {cmp_['digest_mismatches']}, "
                        f"constants compared {cmp_['constants_compared']}, mismatches {cmp_['constant_mismatches']}, "
                        f"sign flips {cmp_['sign_flips']}, missing {cmp_['missing']}, flags {cmp_['singular_flags']}\n"
                        f"--- Singular output ---\n{out}")
        log(f"Singular {tag}: pass={cmp_['pass']} digests={cmp_['digests_compared']} constants={cmp_['constants_compared']}")
    (ART / "singular-check.txt").write_text("\n".join(sing_txt), encoding="utf-8")
    results["gates"]["singular_M9"] = {"pass": bool(sing_ok)}

    # ---- SLPs ----
    for tag, (st, terms) in states.items():
        slp = {"experiment": "EXP-146", "branch": tag, "prime_tree": {"p": prime1.p, "r": prime1.r},
               "prime_replay": {"p": prime2.p, "r": prime2.r}, "order": ORDER,
               "inputs": {mid: [{"exps": e, "coords": cs} for e, cs in tl] for mid, tl in terms.items()},
               "nodes": st.records, "replay": results["replay"][tag]}
        write(ART / f"slp-{tag}.json", slp)

    gate_fail = [k for k, v in results["gates"].items() if isinstance(v, dict) and not v.get("pass", True)]
    if gate_fail:
        return finish(results, f"FAILED gates {gate_fail}", 1)
    if unknown or not all_cert:
        return finish(results, "UNKNOWN", 2)
    results["seconds_total"] = round(time.time() - t_start, 1)
    return finish(results, "CONFIRMED", 0)


if __name__ == "__main__":
    sys.exit(main())
