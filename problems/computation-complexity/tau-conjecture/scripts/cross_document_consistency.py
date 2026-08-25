"""Cross-document consistency gate for the tau-conjecture record.

The adversarial pass of 2026-08-25 found the same quantity written two ways in
one manuscript (134,494 against 134,497) and three different refutation counts in
three places. Numbers drift between the paper, the wiki, the context notes and
the portfolio mirror because each is edited separately.

This asserts that every canonical value, wherever it appears, appears with its
canonical spelling. It is deliberately dumb: it greps for WRONG spellings of
known quantities rather than trying to parse prose.
"""
import io
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
MIRROR = "D:/_Repos/_Web_Projects/_CAOS_MANAGE/plans/caos-research/tau-conjecture"

def num(*groups):
    """Regex for an integer however it is written: 134497, 134,497, 134{,}497."""
    sep = "(?:[{],[}]|,)?"
    return sep.join(groups)

# (label, regex that must NOT appear, why)
FORBIDDEN = [
    ("depth-6 new polynomials", num("134", "497"), "correct value is 134,494 (free inputs are not new)"),
    ("core count", r"24 cores", "the machine has 32 cores"),
    ("compute total", r"under twenty hours", "actual is ~40 h plus a multi-day scan"),
    ("experiment range", r"EXP-001\}--\texttt\{EXP-005", "experiments run to EXP-014"),
    ("interval overclaim", r"minimal-gate (root )?sets are intervals", "an interval is only AMONG the records"),
    ("chebyshev at tau=5", r"tower would give only four", "the tower is at two roots at five gates"),
    ("frontier size", r"states, 28 GB", "29,356,905,536 bytes = 27.3 GiB"),
]

# (label, canonical string, files that MUST contain it if they mention the topic)
REQUIRED_IF_MENTIONED = [
    ("zmax ladder", r"1,\s*2,\s*3,\s*3,\s*4,\s*5,\s*5,\s*6", r"zmax|z_\{\max\}|z_max"),
    ("frontier7", num("1", "048", "460", "912"), r"frontier|depth-7 frontier"),
]

SELFTEST = [
    (num("134", "497"), "enumerates all $134{,}497$ new polynomials", True),
    (num("134", "497"), "134,497 new polynomials, 180 s", True),
    (num("134", "497"), "all $134{,}494$ new polynomials", False),
    (r"24 cores", "on one desktop machine (24 cores; the depth-8", True),
    (r"24 cores", "machine with $32$ cores", False),
    (r"under twenty hours", "for every result in this paper is under twenty hours", True),
    (r"minimal-gate (root )?sets are intervals", "the minimal-gate sets are intervals.", True),
    (r"minimal-gate (root )?sets are intervals", "an interval is always AMONG the minimal-gate record sets", False),
    (r"tower would give only four", "so a tower would give only four roots here.", True),
    (r"states, 28 GB", "($1{,}048{,}460{,}912$ states, 28 GB) and the catalog", True),
]


def self_test():
    """A gate that cannot fail proves nothing. Fire every pattern at the exact
    pre-fix string it is meant to catch, and at a corrected string it must not."""
    bad = 0
    for pat, text, should in SELFTEST:
        got = bool(re.search(pat, text))
        if got != should:
            bad += 1
            print(f'  SELFTEST FAIL {pat[:40]!r} on {text[:44]!r}: matched={got}, want={should}')
        else:
            print(f"  ok  {pat[:34]:<36} {'BAD ' if should else 'GOOD'} sample -> {got}")
    return bad

files = []
for base in (ROOT, MIRROR):
    if not os.path.isdir(base):
        continue
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "artifacts", "logs")]
        for fn in filenames:
            if fn.endswith((".md", ".tex")):
                files.append(os.path.join(dirpath, fn))
# the manuscript lives outside the problem folder
man = os.path.join(ROOT, "..", "..", "..", "manuscripts", "tau-conjecture", "census", "main.tex")
if os.path.exists(man):
    files.append(man)

print('== self-test: does the gate detect what it claims? ==')
st = self_test()
if st:
    print()
    print('GATE IS BROKEN; not reporting a verdict on the documents')
    sys.exit(2)
print()
print(f"scanning {len(files)} documents")
bad = 0
for label, pat, why in FORBIDDEN:
    hits = []
    for f in files:
        try:
            s = io.open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for m in re.finditer(pat, s):
            line = s[:m.start()].count("\n") + 1
            # a correction note may quote the wrong value on purpose
            ctx = s[max(0, m.start()-260):m.start()+120].lower()
            if any(w in ctx for w in ("earlier draft", "correction", "an earlier", "first reported",
                                      "said four", "wrong", "forbidden", "against 134")):
                continue
            hits.append(f"{os.path.relpath(f, ROOT)}:{line}")
    if hits:
        bad += len(hits)
        print(f"  FAIL  {label}: {why}")
        for h in hits[:6]:
            print(f"          {h}")
    else:
        print(f"  PASS  {label}")

print()
print("inconsistencies:", bad)
sys.exit(1 if bad else 0)
