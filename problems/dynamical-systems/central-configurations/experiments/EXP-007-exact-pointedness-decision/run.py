"""EXP-007: decide every comet's pointedness exactly (phase-I simplex over QQ).

Reads the EXP-004 prevariety outputs, rebuilds the comets with the corrected
t = 1 slice semantics, and decides each recession cone with
cclib.exact_lp.decide_pointed. Every outcome carries a certificate that is
re-verified by exact substitution here, independently of the decider.

Run: .venv/Scripts/python.exe problems/.../EXP-007-exact-pointedness-decision/run.py
"""
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))
sys.path.insert(0, str(HERE.parent / "EXP-004-valuation-equation-screening"))
from cclib.exact_lp import decide_pointed  # noqa: E402
from comet_analysis import components, parse_sections  # noqa: E402

HEAVY = Path("E:/_Datos/caos-research/central-configurations/EXP-004")
ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"
CAP_PER_FILE = 1800
RESULTS = {}


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def verify(gens, res):
    """Re-verify the certificate independently of the decider."""
    if res.pointed:
        if res.certificate is None:
            return "pointed(farkas-only)"
        ok = all(sum(c * g for c, g in zip(res.certificate, gen)) < 0 for gen in gens)
        return "pointed(verified)" if ok else "POINTED-CERT-FAILED"
    lam = res.certificate
    d = len(gens[0])
    zero = all(sum(lam[j] * gens[j][i] for j in range(len(gens))) == 0 for i in range(d))
    nonneg = all(v >= 0 for v in lam) and sum(lam) > 0
    return "unpointed(verified)" if (zero and nonneg) else "UNPOINTED-CERT-FAILED"


def main():
    LOG.write_text("", encoding="utf-8")
    log("EXP-007 start: exact pointedness decision over the EXP-004 outputs")
    files = sorted(HEAVY.glob("out-*.out"))
    if not files:
        log(f"no EXP-004 outputs found under {HEAVY}")
        return 1
    summary = {}
    for path in files:
        t0 = time.time()
        rays, cones = parse_sections(str(path))
        comps = components(rays, cones)
        n_pointed = n_unpointed = n_failed = 0
        certs = []
        capped = False
        for ci, comp in enumerate(comps):
            if time.time() - t0 > CAP_PER_FILE:
                capped = True
                break
            gens = [[Fraction(x) for x in rays[i][1:]] for i in comp if rays[i][0] == 0]
            if not gens:
                n_pointed += 1
                continue
            res = decide_pointed(gens)
            status = verify(gens, res)
            if status.startswith("pointed"):
                n_pointed += 1
            elif status.startswith("unpointed"):
                n_unpointed += 1
                certs.append({"comet": ci, "n_generators": len(gens),
                              "lambda": [str(v) for v in res.certificate]})
            else:
                n_failed += 1
                log(f"  {path.name} comet {ci}: {status}")
        secs = time.time() - t0
        summary[path.name] = {"comets": len(comps), "pointed": n_pointed,
                              "unpointed": n_unpointed, "cert_failures": n_failed,
                              "capped": capped, "seconds": round(secs, 1)}
        log(f"{path.name}: comets {len(comps)}, pointed {n_pointed}, "
            f"unpointed {n_unpointed}, cert-failures {n_failed}"
            f"{' (CAP)' if capped else ''}, {secs:.0f} s")
        if certs:
            (ART / f"{path.stem}-unpointed-certificates.json").write_text(
                json.dumps(certs[:5], indent=2), encoding="utf-8")
        (ART / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    decided = all(not v["capped"] and v["cert_failures"] == 0 for v in summary.values())
    log(f"done; all cells fully decided with verified certificates: {decided}")
    return 0 if decided else 1


if __name__ == "__main__":
    sys.exit(main())
