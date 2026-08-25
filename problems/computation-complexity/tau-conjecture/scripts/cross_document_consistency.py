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
    ("frontier size (paper)", r"states, 28 GB", "29,356,905,536 bytes = 27.3 GiB"),
    ("frontier size (notes)", r"frontier7? ?\(?28 GB", "29,356,905,536 bytes = 27.3 GiB"),
    ("catalog entry count", num("2", "161", "169"), "the catalog holds 2,161,049 entries"),
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
    (r"frontier7? ?\(?28 GB", "Data assets: depth-7 frontier (28 GB) + poly catalog", True),
    (r"frontier7? ?\(?28 GB", "depth-7 frontier (27.3 GiB, 29,356,905,536 bytes)", False),
    (num("2", "161", "169"), "interned poly table (2,161,169 entries)", True),
    (num("2", "161", "169"), "interned poly table (2,161,049 entries)", False),
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

# A file whose JOB is to document defects necessarily quotes them. Guessing at
# the phrasings around each quotation was fragile (the first attempt missed
# 'FALSE', '(it is 32)' and 'could not match'), so such a file declares itself
# instead. The declaration is explicit, greppable, and reviewable; ladder checks
# still apply to these files, only the forbidden-string checks are waived.
OPT_OUT = 'consistency-gate: quotes-defects'

# Canonical ladders, each identified by PLAIN SUBSTRINGS that must appear on the
# same line (no regex, so no LaTeX escaping to get wrong).
#
# Keying on the numeric prefix alone is wrong: zmax, zqmax and zrmax all begin
# 1, 2, 3, and the doubling family's degree row begins 4, 8, 16 exactly like its
# real-root row. The first version of this check keyed on the prefix and cried
# wolf four times on correct rows.
OTHER = ('zpmax', 'zrmax', 'zqmax', 'mathbb{F}', 'mathbb{R}', 'mathbb{Q}')
LADDERS = [
    ('zmax over Z',      ('zmax', 'mathbb{Z}'),        OTHER,      [1, 2, 3, 3, 4, 5, 5, 6]),
    ('zpmax over F_p',   ('zpmax', 'mathbb{F}'),       (),         [1, 2, 4, 8, 16, 32, 64, 128]),
    ('zrmax over R',     ('zrmax', 'mathbb{R}'),       (),         [1, 2, 3, 4, 6, 8]),
    ('zqmax over Q',     ('zqmax', 'mathbb{Q}'),       (),         [1, 2, 3, 3, 4, 5]),
    ('odd digit ladder', ('odd',),                     (),         [1, 2, 2, 2, 2, 3, 4]),
    ('mod-3 ladder',     ('mod 3', 'pmod 3', 'mod-3'), (),         [1, 1, 1, 2, 2, 3, 3]),
    ('minimal height',   ('height',),                  (),         [1, 1, 2, 4, 15]),
    ('doubling real',    ('distinct real roots',),     ('degree',),[4, 8, 16, 28, 48]),
]


def check_ladders(files):
    seq_re = re.compile(r'(?<![-0-9.])((?:[0-9]{1,3}[ ]*(?:,|&|[|])[ ]*){3,}[0-9]{1,3})(?![0-9.])')
    bad = 0
    for f in files:
        try:
            txt = io.open(f, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        for ln_no, line in enumerate(txt.split(chr(10)), 1):
            for m in seq_re.finditer(line):
                try:
                    seq = [int(v.strip()) for v in re.split(r'[,&|]', m.group(1)) if v.strip()]
                except ValueError:
                    continue
                if len(seq) < 4:
                    continue
                for name, want, avoid, canon in LADDERS:
                    if not any(w in line for w in want):
                        continue
                    if any(a in line for a in avoid):
                        continue
                    if seq[:3] != canon[:3]:
                        continue
                    if seq != canon[:len(seq)]:
                        print(f'  FAIL  {name}: found {seq} at {os.path.basename(f)}:{ln_no}')
                        print(f'          canonical is {canon}')
                        bad += 1
    if not bad:
        print('  PASS  every labelled ladder row matches its canonical prefix')
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
        if OPT_OUT in s:
            continue
        lines = s.split(chr(10))
        for m in re.finditer(pat, s):
            line_no = s[:m.start()].count(chr(10))
            hits.append(f'{os.path.basename(f)}:{line_no + 1}')
    if hits:
        bad += len(hits)
        print(f"  FAIL  {label}: {why}")
        for h in hits[:6]:
            print(f"          {h}")
    else:
        print(f"  PASS  {label}")

print()
print('== ladder consistency ==')
bad += check_ladders(files)

print()
print("inconsistencies:", bad)
sys.exit(1 if bad else 0)
