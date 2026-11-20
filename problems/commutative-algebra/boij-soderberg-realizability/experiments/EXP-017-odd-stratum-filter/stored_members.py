"""EXP-017, record added after the verdict: the exact filter on every member of the stratum S((e+1)/2; 0, (e-1)/2) that EXP-010 and
EXP-014 stored with a computed Betti table.

The verdict of EXP-017 states the count (130 members with a table: the 59 pure ones pass, the 71 others do not); the results of the
run hold only the 59 pure members (gate G3). This script recomputes the count from the committed artifacts of EXP-010 and EXP-014 with
the filter of `exp017_routine` and writes it to `artifacts/stored-members-filter.json`, so that the count is read from an artifact.
It runs no search and changes no result of the experiment.

    python stored_members.py            write the artifact
    python stored_members.py --check    recompute and compare with the committed artifact (exit 1 on a difference)
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPS = HERE.parent
sys.path.insert(0, str(HERE))

import exp017_routine as R  # noqa: E402

OUT = HERE / "artifacts" / "stored-members-filter.json"
SOURCES = ["EXP-010-weight-class-strata", "EXP-014-middle-strata"]
STAGES = ["fails F0", "fails F1", "fails F2", "fails F3", "passes"]


def compute():
    """The filter on every stored member with a computed table (the flag `pure` is True or False), for every stratum of that shape with
    stored members in the results of the two experiments, per stratum and in total."""
    rows = []
    for name in SOURCES:
        res = json.loads((EXPS / name / "artifacts" / "results.json").read_text(encoding="utf-8"))
        for key, st in res["strata"].items():
            e, p = st["e"], st["p"]
            if e % 2 == 0 or (st["m"], st["i"], st["j"]) != ((e + 1) // 2, 0, (e - 1) // 2) or not st.get("members"):
                continue
            row = {"source": name, "stratum": key, "e": e, "p": p, "stored": len(st["members"]), "tabled": 0, "pure": 0, "other": 0,
                   "not_of_the_form": 0, "pure_by_stage": [0] * 5, "other_by_stage": [0] * 5}
            for mem in st["members"]:
                if mem.get("pure") not in (True, False):
                    continue
                row["tabled"] += 1
                kind = "pure" if mem["pure"] else "other"
                row[kind] += 1
                ab = R.alpha_beta_of_pair(e, p, mem["f"], mem["g"])
                if ab is None:
                    row["not_of_the_form"] += 1
                    continue
                stage = R.filter_member(e, p, *ab)[0]
                row[kind + "_by_stage"][stage] += 1
            rows.append(row)
    tot = {k: sum(r[k] for r in rows) for k in ("stored", "tabled", "pure", "other", "not_of_the_form")}
    for kind in ("pure", "other"):
        tot[kind + "_by_stage"] = [sum(r[kind + "_by_stage"][s] for r in rows) for s in range(5)]
    return {
        "experiment": "EXP-017-odd-stratum-filter",
        "record": "the exact filter (F0) to (F3) on the members of S((e+1)/2; 0, (e-1)/2) stored by EXP-010 and EXP-014 with a computed "
                  "Betti table; added after the verdict, computed from the committed artifacts of the two experiments",
        "stages": STAGES,
        "pairs": sorted({(r["e"], r["p"]) for r in rows}),
        "rows": rows,
        "totals": tot,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare with the committed artifact instead of writing it")
    args = ap.parse_args()
    data = json.loads(json.dumps(compute()))
    t = data["totals"]
    print(f"stored {t['stored']}, with a table {t['tabled']}: pure {t['pure']} {t['pure_by_stage']}, other {t['other']} "
          f"{t['other_by_stage']}, not of the form {t['not_of_the_form']}; pairs {len(data['pairs'])}")
    if args.check:
        old = json.loads(OUT.read_text(encoding="utf-8"))
        if old != data:
            print("DIFFERENT from", OUT.name)
            return 1
        print("artifact current")
        return 0
    OUT.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8", newline="\n")
    print("wrote", OUT.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
