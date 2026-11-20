"""EXP-008 routine: the families A, B, C of the frozen hypothesis on top of the routine of EXP-006 (imported, not edited).

EXP-006's `exp006_routine` already takes e as a parameter (structure constants, rank of mu_n(W), Hilbert function,
Betti table through `uhlib`, the seeded generator), so the only pieces written here are the three families, the chunk
worker that stores only what the hypothesis asks and the early-stop bookkeeping.  Seeds: 20261120 + index inside a
family and field (EXP-006's `SEED_BASE`).
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "EXP-006-odd-characteristic-below-2e"
if str(SIBLING) not in sys.path:
    sys.path.insert(0, str(SIBLING))

import exp006_routine as R  # noqa: E402

SEED_BASE = R.SEED_BASE  # 20261120
EARLY_STOP = 40
# family: (e, field, spaces planned, chunk size)
FAMILIES = {
    "A": (5, "GF(5)", 150000, 250),
    "B": (5, "GF(7)", 300000, 250),
    "C": (6, "GF(3)", 1000000, 500),
}


def chunk_id(family, start, end):
    return "%s|%05d-%07d" % (family, start, end)


def chunk_specs(only=None):
    out = []
    for fam, (e, fname, n, chunk) in FAMILIES.items():
        if only and fam not in only:
            continue
        for s in range(0, n, chunk):
            t = min(s + chunk, n)
            out.append({"id": chunk_id(fam, s, t), "family": fam, "field": fname, "e": e, "start": s, "end": t})
    return out


def space_of(fname, e, index):
    """The space of a given index of a family: the same seed always gives the same space."""
    F = R.make_field(fname)
    return F, R.draw_space(F, e, SEED_BASE + index)


def run_chunk(spec):
    """Evaluate the spaces start..end-1.  Stored per chunk: the distribution of rank mu_3e, the counts, and every space with
    the pure Hilbert function (index, seed, ranks, Betti table; the basis only when pure).  Nothing per space otherwise."""
    t0 = time.time()
    F = R.make_field(spec["field"])
    e = spec["e"]
    agg = {"id": spec["id"], "family": spec["family"], "field": spec["field"], "e": e, "start": spec["start"],
           "end": spec["end"], "n": 0, "rank_hist": {}, "hilbert_computed": 0, "hilbert_other": {}, "pure_hilbert": 0,
           "pure": 0, "nonpure_tables": {}, "spaces": []}
    for idx in range(spec["start"], spec["end"]):
        seed = SEED_BASE + idx
        C = R.draw_space(F, e, seed)
        ev = R.evaluate(F, C, e, "A")
        key = str(ev["rank3e"])
        agg["n"] += 1
        agg["rank_hist"][key] = agg["rank_hist"].get(key, 0) + 1
        if ev["hilbert"] is not None:
            agg["hilbert_computed"] += 1
            if not ev["pure_hilbert"]:
                hk = ",".join(str(x) for x in ev["hilbert"])
                agg["hilbert_other"][hk] = agg["hilbert_other"].get(hk, 0) + 1
        agg["pure_hilbert"] += ev["pure_hilbert"]
        agg["pure"] += ev["pure"]
        if ev["pure_hilbert"]:
            if not ev["pure"]:
                bk = str(ev["betti"])
                agg["nonpure_tables"][bk] = agg["nonpure_tables"].get(bk, 0) + 1
            rec = {"index": idx, "seed": seed, "rank3e": ev["rank3e"], "pure": ev["pure"], "betti": ev["betti"]}
            if ev["pure"]:
                rec["basis"] = R.basis_json(F, C, e)
            agg["spaces"].append(rec)
    agg["seconds"] = round(time.time() - t0, 2)
    return agg


class EarlyStop:
    """Bookkeeping of the early stop of a family: chunks are handed out in index order; once the finished chunks hold
    `limit` pure spaces no further chunk is handed out, chunks already running finish and are counted."""

    def __init__(self, limit=EARLY_STOP):
        self.limit = limit
        self.pure = 0

    def add(self, chunk_pure):
        self.pure += chunk_pure

    @property
    def stopped(self):
        return self.pure >= self.limit
